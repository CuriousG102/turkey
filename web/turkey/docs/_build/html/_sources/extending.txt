Writing Your Own Steps and Auditors
***********************************

Steps
=====
If you think of your HIT as a test, then a "step" is an individual question in your test. You can add as many
steps as you would like to your task, and you can choose to have them ordered or unordered (randomized). The
same applies to the response options of each step, if applicable.]

Currently Included Steps
------------------------
Multiple Answer
+++++++++++++++
Checkbox questions that allows the worker to select several answers.

Multiple Choice
+++++++++++++++
Classic multiple choice question that restricts the worker to selecting only one answer.

Text Input
++++++++++
Question that requires the worker to typing a response.

Writing Your Own
----------------
Writing your own steps will involve several steps. You will need to add Python code, generate migrations, and have
associated Python, HTML, and Javascript .. TODO Have a full walkthrough

Python
++++++
Models for steps are in

.. automodule:: survey.steps
   :members:
   :undoc-members:

Add your step to the dictionary "NAME_TO_STEP" at the top of the file. You will need to write two classes,
one for the step's data and one for the step itself. The data class will have a "general_models" field with
the foreign key being the name of your step and a "response" field specifying the type of response your database
should expect to receive (int, text, etc). The step class has a "script_location" field, a "template_file"
location field, a "data_model" field (which is simply the data class you just wrote), and some metadata fields
specific to an instance of this step such as "title" and "text" (question text). Fields in this class will affect
how the process of adding this step will appear on the admin site. Note that a step's fields can be accessed in a
template with step_instance.attribute; this can be helpful when filling out HTML element fields.Sp

