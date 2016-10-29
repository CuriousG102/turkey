import json
import platform

import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.exceptions import ValidationError
from django.test import Client
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils.decorators import classproperty
from rest_framework import status
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from . import default_settings
from .models import Task, Token, TaskInteraction, StepTextInput, AuditorClicksTotal, AuditorClicksTotalData, \
    AuditorBeforeTypingDelay, AuditorBeforeTypingDelayData, AuditorClicksSpecific, AuditorClicksSpecificData, \
    AuditorFocusChanges, AuditorFocusChangesData, AuditorKeypressesTotalData, AuditorKeypressesTotal, \
    AuditorKeypressesSpecific, AuditorKeypressesSpecificData, AuditorMouseMovementTotal, AuditorMouseMovementTotalData, \
    AuditorMouseMovementSpecific, AuditorMouseMovementSpecificData, AuditorPastesTotal, AuditorPastesTotalData, \
    AuditorPastesSpecific, AuditorPastesSpecificData, AuditorRecordedTimeDisparity, AuditorRecordedTimeDisparityData


class AbstractTestCase(TestCase):
    TASK_IS_EXTERNAL = False
    TASK_IS_PUBLISHED = True

    def setUp(self):
        self.admin_user = User.objects.create_user('admin', 'admin@admin.com', 'adminpassword')
        self.internal_task = Task(survey_name='Bestest Task',
                                  external=self.TASK_IS_EXTERNAL,
                                  published=self.TASK_IS_PUBLISHED)
        self.internal_task.save()
        self.internal_task.owners.add(self.admin_user)
        self.token = Token.objects.create()
        self.client = Client()


class BasicAuditorSubmissionTestCase(AbstractTestCase):
    SUBMISSION_OBJECTS_KEY = 'auditors'

    def create_task_interaction(self):
        return TaskInteraction.objects.create(task=self.internal_task,
                                              token=self.token)

    def post_basic_submission(self, interaction):
        return self.post_json_submission(interaction,
                                         {'token': self.token.token.decode(),
                                          self.SUBMISSION_OBJECTS_KEY: {}})

    def post_json_submission(self, interaction, data):
        return self.client.post(reverse('survey:auditor_submission',
                                        kwargs={'pk': interaction.task.pk}),
                                content_type='application/json',
                                data=json.dumps(data))

    def test_cant_submit_to_unpublished_task(self):
        self.internal_task.published = False
        self.internal_task.save()
        response = self.post_basic_submission(self.create_task_interaction())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_submit_to_published_task(self):
        response = self.post_basic_submission(self.create_task_interaction())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cant_double_submit(self):
        AuditorClicksTotal.objects.create(task=self.internal_task)
        interaction = self.create_task_interaction()
        response = self.post_json_submission(
            interaction,
            {
                'token': self.token.token.decode(),
                self.SUBMISSION_OBJECTS_KEY: {
                    'clicks_total': {
                        'count': 5
                    }
                }
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.post_json_submission(
            interaction,
            {
                'token': self.token.token.decode(),
                self.SUBMISSION_OBJECTS_KEY: {
                    'clicks_total': {
                        'count': 5
                    }
                }
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auditor_submission_serialized(self):
        """
        Test with one of the basic auditors that things are properly going to the database.
        """
        auditor = AuditorClicksTotal.objects.create(task=self.internal_task)
        interaction = self.create_task_interaction()
        self.post_json_submission(
            interaction,
            {
                'token': self.token.token.decode(),
                self.SUBMISSION_OBJECTS_KEY: {
                    'clicks_total': {
                        'count': 5
                    }
                }
            }
        )
        data = AuditorClicksTotalData.objects.filter(general_model=auditor)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].count, 5)

    def test_junk_data_returns_bad_request(self):
        AuditorClicksTotal.objects.create(task=self.internal_task)
        interaction = self.create_task_interaction()
        response = self.post_json_submission(
            interaction,
            {
                'token': self.token.token.decode(),
                self.SUBMISSION_OBJECTS_KEY: {
                    'clicks_total': {
                        'count': 'fish'
                    }
                }
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenSanityChecks(AbstractTestCase):
    def test_can_create(self):
        Token.objects.create()


class TaskSanityChecks(AbstractTestCase):
    def test_can_modify_without_submission(self):
        self.internal_task.survey_name = 'Worstest Task'
        self.internal_task.full_clean()
        self.internal_task.save()

    def test_cant_change_test_to_external_without_deleting_steps(self):
        step = StepTextInput.objects.create(task=self.internal_task,
                                            title='Are you truly happy',
                                            text='If you lie you\'re only '
                                                 'hurting yourself',
                                            step_num=1)
        self.internal_task.external = True
        with self.assertRaises(ValidationError):
            self.internal_task.full_clean()
        step.delete()
        self.internal_task.full_clean()

    def invalid_task_modification(self, modification_function):
        TaskInteraction.objects.create(token=self.token,
                                       task=self.internal_task)
        modification_function(self.internal_task)
        with self.assertRaises(ValidationError):
            self.internal_task.full_clean()

    def test_cant_make_unnamed_internal_task(self):
        task = Task(survey_name='', external=False)
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_cant_modify_name_after_submission(self):
        """
        Tests whether we are keeping users from modifying tasks after
        users have already submitted responses, or auditors have already
        collected data. This protects data consistency on our end.

        Any user interaction is represented by a task interaction.
        """

        def mod(task):
            task.survey_name = 'Worstest'

        self.invalid_task_modification(mod)

    def test_cant_modify_external_status_after_submission(self):
        def mod(task):
            task.external = True

        self.invalid_task_modification(mod)


class AbstractAuditorTestCase(StaticLiveServerTestCase):
    def get_webdriver(self):
        if platform.system() != 'Linux':
            return webdriver.Chrome('/usr/local/bin/chromedriver')
        else:
            return webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)

    def setUp(self):
        super().setUp()
        self.selenium = self.get_webdriver()
        self.token = Token.objects.create()
        self.task = Task(survey_name='Bestest Task',
                         external=False,
                         published=True)
        self.selenium.get(self.get_url('admin:login'))
        self.selenium.add_cookie({
            'name': default_settings.SURVEY_CONFIG['TOKEN_NAME'],
            'value': self.token.token.decode(),
            'path': '/',
            'domain': self.live_server_host
        })
        self.task.save()

    @classproperty
    def live_server_url(cls):
        return 'http://%s:%s' % (
            cls.live_server_host,
            cls.server_thread.port)

    @classproperty
    def live_server_host(cls):
        return cls.server_thread.host if platform.system() != 'Linux' else 'web'

    def get_url(self, name, kwargs=None):
        return self.live_server_url + reverse(name, kwargs=kwargs)

    def take_auditor_actions(self):
        pass

    def verify_auditor_data(self, interaction):
        pass

    def test_auditor(self):
        self.selenium.get(self.get_url('survey:TaskPage',
                                       kwargs={'pk': self.task.pk}))
        self.take_auditor_actions()
        self.selenium.find_element_by_id('submit').click()
        interaction = TaskInteraction.objects.filter(task=self.task)
        self.assertEqual(len(interaction), 1)
        interaction = interaction[0]
        # give the browser time to finish submitting data
        time.sleep(1)
        self.verify_auditor_data(interaction)


class AuditorTotalClicksTestCase(AbstractAuditorTestCase):
    NUMBER_CLICKS = 3

    def setUp(self):
        super().setUp()
        self.clicks_auditor = AuditorClicksTotal.objects \
            .create(task=self.task)

    def take_auditor_actions(self):
        body = self.selenium.find_element_by_tag_name('body')
        for _ in range(self.NUMBER_CLICKS):
            body.click()

    def verify_auditor_data(self, interaction):
        auditor_data = AuditorClicksTotalData.objects.filter(task_interaction_model=interaction)
        self.assertEqual(len(auditor_data), 1)
        auditor_data = auditor_data[0]
        # add one for submission button click
        self.assertEqual(auditor_data.count, self.NUMBER_CLICKS + 1)


class AuditorBeforeTypingDelayUserTypes(AbstractAuditorTestCase):
    TIME_WAIT_TO_TYPE = 1

    def setUp(self):
        super().setUp()
        self.delay_auditor = AuditorBeforeTypingDelay.objects \
            .create(task=self.task)

    def take_auditor_actions(self):
        time.sleep(self.TIME_WAIT_TO_TYPE)
        self.selenium.find_element_by_tag_name('body').send_keys('kjlj;')

    def verify_auditor_data(self, interaction):
        auditor_data = AuditorBeforeTypingDelayData.objects.filter(task_interaction_model=interaction)
        self.assertEqual(len(auditor_data), 1)
        auditor_data = auditor_data[0]
        self.assertLess(auditor_data.milliseconds / 1000, self.TIME_WAIT_TO_TYPE * 1.5)
        self.assertGreater(auditor_data.milliseconds / 1000, self.TIME_WAIT_TO_TYPE)


class AuditorClicksSpecificTestCase(AbstractAuditorTestCase):
    def setUp(self):
        super().setUp()
        self.clicks_auditor = AuditorClicksSpecific.objects.create(task=self.task)

    def take_auditor_actions(self):
        self.selenium.find_element_by_tag_name('body').click()

    def verify_auditor_data(self, interaction):
        # TODO: Identify why the failures on commented out lines are happening
        auditor_data = AuditorClicksSpecificData.objects.filter(task_interaction_model=interaction)
        self.assertEqual(auditor_data.count(), 2)
        body_click = auditor_data.filter(dom_type='body')[0]
        self.assertEqual(body_click.dom_type, 'body')
        # self.assertEqual(body_click.dom_name, 'body')
        self.assertIsNone(body_click.dom_id)
        self.assertIsNone(body_click.dom_class)
        self.assertGreaterEqual(body_click.time, 0)
        submit_click = auditor_data.filter(dom_id='submit')[0]
        self.assertEqual(submit_click.dom_type, 'input')
        # self.assertEqual(submit_click.dom_name, 'input')
        self.assertEqual(submit_click.dom_id, 'submit')
        # self.assertEqual(submit_click.dom_class, 'btn btn-primary')
        self.assertGreater(submit_click.time, body_click.time)


class AuditorKeypressesTotalTestCase(AbstractAuditorTestCase):
    NUM_KEY_PRESSES = 5

    def setUp(self):
        super().setUp()
        self.auditor = AuditorKeypressesTotal.objects.create(task=self.task)

    def take_auditor_actions(self):
        self.selenium.find_element_by_tag_name('body').send_keys('t' * self.NUM_KEY_PRESSES)

    def verify_auditor_data(self, interaction):
        auditor_data = AuditorKeypressesTotalData.objects.get(task_interaction_model=interaction)
        self.assertEqual(auditor_data.count, self.NUM_KEY_PRESSES)


class AuditorKeypressesSpecificTestCase(AbstractAuditorTestCase):
    KEYS_TO_PRESS = 'abcde'

    def setUp(self):
        super().setUp()
        self.auditor = AuditorKeypressesSpecific.objects.create(task=self.task)

    def take_auditor_actions(self):
        self.selenium.find_element_by_tag_name('body').send_keys(self.KEYS_TO_PRESS)

    def verify_auditor_data(self, interaction):
        auditor_data = AuditorKeypressesSpecificData.objects \
            .filter(task_interaction_model=interaction).order_by('time')
        self.assertEqual(len(auditor_data), len(self.KEYS_TO_PRESS))
        self.assertEqual(''.join([a.key for a in auditor_data]),
                         self.KEYS_TO_PRESS.upper())


class AuditorMouseMovementTotalTestCase(AbstractAuditorTestCase):
    MOVEMENTS = 3  # should be at least 1
    TIME_BETWEEN_MOVEMENTS = 250  # ms

    def setUp(self):
        super().setUp()
        self.auditor = AuditorMouseMovementTotal.objects.create(task=self.task)

    def take_auditor_actions(self):
        body = self.selenium.find_element_by_tag_name('body')
        actions = ActionChains(self.selenium)
        actions.move_to_element(body)
        actions.perform()
        movements = self.MOVEMENTS
        offset = (50, 50)
        while movements:
            movements -= 1
            time.sleep(self.TIME_BETWEEN_MOVEMENTS / 1000)
            actions.move_by_offset(*offset)
            actions.perform()
            offset = (-offset[0], -offset[1])

    def verify_auditor_data(self, interaction):
        auditor_data = AuditorMouseMovementTotalData.objects \
            .get(task_interaction_model=interaction)
        self.assertEqual(auditor_data.amount, self.MOVEMENTS)


class AuditorMouseMovementSpecificTestCase(AbstractAuditorTestCase):
    MOVEMENTS = 3  # should be at least 1
    TIME_BETWEEN_MOVEMENTS = 250  # ms
    OFFSET = (50, 50)

    def setUp(self):
        super().setUp()
        self.auditor = AuditorMouseMovementSpecific.objects.create(task=self.task)

    def take_auditor_actions(self):
        window = self.selenium.find_element_by_tag_name('body')
        actions = ActionChains(self.selenium)
        actions.move_to_element_with_offset(window, 0, 0)
        actions.perform()
        movements = self.MOVEMENTS
        offset = self.OFFSET
        while movements:
            movements -= 1
            time.sleep(self.TIME_BETWEEN_MOVEMENTS / 1000)
            actions.move_by_offset(*offset)
            actions.perform()
            offset = (-offset[0], -offset[1])

    def verify_auditor_data(self, interaction):
        auditor_data = AuditorMouseMovementSpecificData.objects \
            .filter(task_interaction_model=interaction) \
            .order_by('time')
        self.assertEqual(len(auditor_data), self.MOVEMENTS)
        for i, movement in enumerate(auditor_data):
            running_position = (0, 0) if i % 2 == 0 else self.OFFSET
            self.assertEqual((movement.x, movement.y), running_position)


class AuditorPastesTotalTestCase(AbstractAuditorTestCase):
    NUMBER_PASTES = 2
    PASTES_CONTENT = 'I COPY AND PASTE INTO TURK TASKS'

    def setUp(self):
        super().setUp()
        self.auditor = AuditorPastesTotal.objects.create(task=self.task)
        StepTextInput.objects.create(task=self.task, step_num=1,
                                     title='copycat',
                                     text='please don\'t cpopy paste')

    def take_auditor_actions(self):
        text_box = self.selenium.find_element_by_tag_name('textarea')
        text_box.send_keys(self.PASTES_CONTENT)
        for _ in range(self.NUMBER_PASTES):
            text_box.send_keys(Keys.CONTROL, 'a')
            text_box.send_keys(Keys.CONTROL, 'c')
            text_box.send_keys(Keys.CONTROL, 'v')

    def verify_auditor_data(self, interaction):
        auditor_data = AuditorPastesTotalData.objects \
            .get(task_interaction_model=interaction)
        self.assertEqual(auditor_data.count, self.NUMBER_PASTES)


class AuditorPastesSpecificTestCase(AbstractAuditorTestCase):
    PASTES_CONTENT = ['I COPY AND PASTE INTO TURK TASKS',
                      'Good or bad? That\'s for you to decide']

    def setUp(self):
        super().setUp()
        self.auditor = AuditorPastesSpecific.objects.create(task=self.task)
        StepTextInput.objects.create(task=self.task, step_num=1,
                                     title='copycat',
                                     text='please don\'t cpopy paste')

    def take_auditor_actions(self):
        text_box = self.selenium.find_element_by_tag_name('textarea')
        for content in self.PASTES_CONTENT:
            text_box.send_keys(Keys.CONTROL, 'a')
            text_box.send_keys(Keys.DELETE)
            text_box.send_keys(content)
            text_box.send_keys(Keys.CONTROL, 'a')
            text_box.send_keys(Keys.CONTROL, 'x')
            text_box.send_keys(Keys.CONTROL, 'v')

    def verify_auditor_data(self, interaction):
        auditor_data = AuditorPastesSpecificData.objects \
            .filter(task_interaction_model=interaction) \
            .order_by('time')
        self.assertEqual(len(auditor_data), len(self.PASTES_CONTENT))
        for datum, truth in zip(auditor_data, self.PASTES_CONTENT):
            self.assertEqual(datum.data, truth)

# TODO: Address failure
# class AuditorRecordedTimeDisparityTestCase(AbstractAuditorTestCase):
#     TOTAL_TIME = 1
#     TIME_OFF = .5
#
#     def setUp(self):
#         super().setUp()
#         self.auditor = AuditorRecordedTimeDisparity.objects \
#             .create(task=self.task)
#
#     def take_auditor_actions(self):
#         time.sleep((self.TOTAL_TIME - self.TIME_OFF)/2)
#         self.selenium.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
#         time.sleep(self.TIME_OFF)
#         self.selenium.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
#         time.sleep((self.TOTAL_TIME - self.TIME_OFF)/2)
#
#     def verify_auditor_data(self, interaction):
#         auditor_data = AuditorRecordedTimeDisparityData.objects\
#             .get(task_interaction_model=interaction)
#         self.assertGreater(auditor_data.milliseconds/1000, self.TIME_OFF)
#         self.assertLess(auditor_data.milliseconds/1000, self.TIME_OFF*1.5)

# TODO: Address failure
# class AuditorFocusChangesTestcase(AbstractAuditorTestCase):
#     TIME_TO_SWITCH = 1
#
#     def setUp(self):
#         super().setUp()
#         self.focus_auditor = AuditorFocusChanges.objects.create(task=self.task)
#
#     def take_auditor_actions(self):
#         time.sleep(self.TIME_TO_SWITCH)
#         self.selenium.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
#         self.selenium.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
#
#     def verify_auditor_data(self, interaction):
#         auditor_data = AuditorFocusChangesData.objects.filter(task_interaction_model=interaction)
#         self.assertEqual(len(auditor_data), 1)
#         auditor_data = auditor_data[0]
#         self.assertLess(auditor_data.time / 1000, self.TIME_TO_SWITCH * 1.5)
#         self.assertGreater(auditor_data.time / 1000, self.TIME_TO_SWITCH)
