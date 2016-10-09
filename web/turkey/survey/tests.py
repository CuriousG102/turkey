from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from .models import Task, Token, TaskInteraction, StepTextInput


class AbstractTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user('admin', 'admin@admin.com', 'adminpassword')

class TokenSanityChecks(AbstractTestCase):
    def test_can_create(self):
        Token.objects.create()

class TaskSanityChecks(AbstractTestCase):
    def setUp(self):
        super().setUp()
        self.internal_task = Task(survey_name='Bestest Task',
                                  external=False,
                                  published=True)
        self.internal_task.save()
        self.internal_task.owners.add(self.admin_user)
        self.token = Token.objects.create()

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

    def test_cant_unpublish(self):
        def mod(task):
            task.published = False

        self.invalid_task_modification(mod)
