from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from .models import Task, Token, TaskInteraction


class AbstractTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user('admin', 'admin@admin.com', 'adminpassword')


class TaskSanityChecks(AbstractTestCase):
    def setUp(self):
        super().setUp()
        self.task = Task(survey_name='Bestest Task',
                         external=False)
        self.task.save()
        self.task.owners.add(
            User.objects.create_user('admin1234', 'admin@admin.com', 'adminpassword')
        )

    def test_cant_modify_after_submission(self):
        """
        Tests whether we are keeping users from modifying tasks after
        users have already submitted responses, or auditors have already
        collected data. This protects data consistency on our end.

        Any user interaction is represented by a task interaction.
        """
        TaskInteraction.objects.create(token=Token.objects.create(),
                                       task=self.task)
        # assert that the below creates a ValidationError
        self.task.survey_name = 'Worstest Task'
        with self.assertRaises(ValidationError):
            self.task.full_clean()
