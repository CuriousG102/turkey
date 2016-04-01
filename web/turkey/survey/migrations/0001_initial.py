# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-27 04:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import survey.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditorBeforeTypingDelay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name_plural': 'Auditors: Before Typing Delay',
                'verbose_name': 'Auditor: Before Typing Delay',
                'ordering': ['task', '-updated', '-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AuditorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'abstract': False,
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='AuditorTotalTaskTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name_plural': 'Auditors: Total Task Time',
                'verbose_name': 'Auditor: Total Task Time',
                'ordering': ['task', '-updated', '-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StepData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'abstract': False,
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='StepMultipleChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('step_num', models.IntegerField(help_text='Controls the order that steps linked to a task are to be taken in by the user', verbose_name='Step Number')),
                ('title', models.CharField(help_text='Title for multiple choice prompt. Choose carefully. This and associated responses are not allowed to change after the first user has responded to this multiple choice step. Then, you must create a new Multiple Choice Step', max_length=144, verbose_name='Title')),
                ('text', models.TextField(help_text='The text to go along with your multiple choice prompt. Choose carefully. This and associated responses are not allowed to change after the first user has responded to this multiple choice step. Then, you must create a new Multiple Choice Step', verbose_name='Multiple Choice Text')),
                ('randomize_order', models.BooleanField(default=False, help_text='Randomizes the order in which responses are presented to the user under a Multiple Choice Step if selected', verbose_name='Randomize Response Order')),
            ],
            options={
                'verbose_name_plural': 'Steps',
                'verbose_name': 'Multiple Choice Step',
                'ordering': ['task', 'step_num', '-updated', '-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StepMultipleChoiceResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('text', models.TextField(help_text='Text for one of the responses to a Multiple Choice Step', verbose_name='Multiple Choice Response Text')),
                ('order', models.IntegerField(blank=True, help_text='Controls the order that responses linked to a Multiple Choice Step are to be rendered. The field can be left blank but this only really makes sense if you randomize order of responses in the Multiple Choice Step', null=True, verbose_name='Response Number')),
                ('multiple_choice_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.StepMultipleChoice', verbose_name='Associated Multiple Choice Step for Response')),
            ],
            options={
                'verbose_name_plural': 'Steps',
                'verbose_name': 'Multiple Choice Step Response',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('number_simultaneous_users', models.IntegerField(help_text='Number of users who need to be in the lobby and ready to begin before they may start the task', validators=[survey.models.not_less_than_one], verbose_name='Number of simultaneous users')),
                ('survey_name', models.CharField(help_text="This is exposed to the user: Name of the survey they're taking", max_length=144, verbose_name='Survey Name')),
                ('owners', models.ManyToManyField(help_text='Users with permission to view and modify', to=settings.AUTH_USER_MODEL, verbose_name='Owners')),
                ('task_dependencies', models.ManyToManyField(blank=True, help_text='Tasks that must be completed before this task by a given user', to='survey.Task', verbose_name='Task Dependencies')),
            ],
            options={
                'verbose_name': 'Interactive Task',
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='TaskInteraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('task', models.ForeignKey(help_text='Task that this is linked to', on_delete=django.db.models.deletion.CASCADE, to='survey.Task', verbose_name='Associated Task')),
            ],
            options={
                'verbose_name': 'Task Interaction',
            },
        ),
        migrations.CreateModel(
            name='AuditorBeforeTypingDelayData',
            fields=[
                ('auditordata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.AuditorData')),
                ('milliseconds', models.IntegerField(help_text='total time in milliseconds that the usertook before typing', null=True, verbose_name='total task time')),
            ],
            options={
                'abstract': False,
                'ordering': ['-updated', '-created'],
            },
            bases=('survey.auditordata',),
        ),
        migrations.CreateModel(
            name='AuditorTotalTaskTimeData',
            fields=[
                ('auditordata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.AuditorData')),
                ('milliseconds', models.IntegerField(help_text='total time in milliseconds that the userspent on the task page', verbose_name='total task time')),
            ],
            options={
                'abstract': False,
                'ordering': ['-updated', '-created'],
            },
            bases=('survey.auditordata',),
        ),
        migrations.CreateModel(
            name='StepMultipleChoiceData',
            fields=[
                ('stepdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.StepData')),
            ],
            options={
                'abstract': False,
                'ordering': ['-updated', '-created'],
            },
            bases=('survey.stepdata',),
        ),
        migrations.AddField(
            model_name='stepmultiplechoice',
            name='task',
            field=models.ForeignKey(help_text='Task that this is linked to', on_delete=django.db.models.deletion.CASCADE, to='survey.Task', verbose_name='Associated Task'),
        ),
        migrations.AddField(
            model_name='stepdata',
            name='task_interaction_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.TaskInteraction'),
        ),
        migrations.AddField(
            model_name='auditortotaltasktime',
            name='task',
            field=models.ForeignKey(help_text='Task that this is linked to', on_delete=django.db.models.deletion.CASCADE, to='survey.Task', verbose_name='Associated Task'),
        ),
        migrations.AddField(
            model_name='auditordata',
            name='task_interaction_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.TaskInteraction'),
        ),
        migrations.AddField(
            model_name='auditorbeforetypingdelay',
            name='task',
            field=models.ForeignKey(help_text='Task that this is linked to', on_delete=django.db.models.deletion.CASCADE, to='survey.Task', verbose_name='Associated Task'),
        ),
        migrations.AddField(
            model_name='stepmultiplechoicedata',
            name='general_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.StepMultipleChoice'),
        ),
        migrations.AddField(
            model_name='stepmultiplechoicedata',
            name='response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.StepMultipleChoiceResponse'),
        ),
        migrations.AddField(
            model_name='auditortotaltasktimedata',
            name='general_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.AuditorTotalTaskTime'),
        ),
        migrations.AddField(
            model_name='auditorbeforetypingdelaydata',
            name='general_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.AuditorBeforeTypingDelay'),
        ),
    ]