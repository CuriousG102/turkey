Contributing and Extending
**************************
MmmTurkey was designed to be modular with the ability to easily add new steps and auditors. If you would like to share your custom steps and auditors and add them to the MmmTurkey project, please feel free to submit a `pull request <https://github.com/CuriousG102/turkey/pulls>`_. Other ways to contribute include writing unit tests and helping out with the docs.

Steps
=====
If you think of your HIT as a test, then a "step" is an individual question in your test. You can add as many steps as you would like to your task, and you can choose to have them ordered or unordered (randomized). The same applies to the response options of each step, if applicable. Writing your own steps will involve several steps. You will need to add Python code, generate migrations, and have associated Python, HTML, and JavaScript.

.. TODO Have a full walkthrough

Python
------
.. Models for steps are in

Add your step to the dictionary ``NAME_TO_STEP`` at the top of the file. You will need to write two classes, one for the step's data and one for the step itself. The data class will have a "general_models" field with the foreign key being the name of your step and a "response" field specifying the type of response your database should expect to receive (int, text, etc). The step class has a "script_location" field, a "template_file" location field, a "data_model" field (which is simply the data class you just wrote), and some metadata fields specific to an instance of this step such as "title" and "text" (question text). Fields in this class will affect how the process of adding this step will appear on the admin site. Note that a step's fields can be accessed in a template with step_instance.attribute; this can be helpful when filling out HTML element fields.

JavaScript
----------
Scripts are located in ``turkey/web/turkey/survey/static/survey/js/``. Create an object with a ``submit_callable`` function that returns an object. This object should get the responses of every instance of this specific step type, and each instance's response should be paired with its primary key in the return object. jQuery should be extremely helpful in extracting the responses of a step instance. After writing this object, be sure to register your step to the "SubmissionHandler" object in ``submission_handler.js``, which handles the submission of results and all auditor data when the submit button is clicked.

.. HTML and CSS
.. ------------
.. TODO

Auditors
========
.. Models for auditors are in

Inspired by the `work <http://jeffrz.com/wp-content/uploads/2010/08/fp359-rzeszotarski.pdf>`_ of Jeff Rzeszotarski and Aniket Kittur, the framework provides "auditor" objects that record a worker's interactions with a task from the moment they start until they submit their responses or close out of the page. Auditor data can be used to analyze worker behavior and estimate the quality of responses. Doing this can potentially help identify bad response data or observe a behavioral pattern amongst workers. Auditors are written in JavaScript and primarily make use of jQuery events to detect browser interactions. Auditor code can be found in ``.../js/auditors``. As with steps, writing auditors consists of several steps.

JavaScript
----------
Auditors generally have the same format, and referencing the default auditors can be helpful when trying to write your own. Create a JavaScript auditor object (``.../js/auditors/``) with your needed fields, a function that modifies those fields, and a function to submit those fields. The modifier function is the action that should be executed when your auditor detects a certain interaction. The submission function (``submit_callable``) must return a JavaScript object or array of JavaScript objects. The fields can have the value of a single value (int, string, etc). Be sure to register your auditor to the "SubmissionHandler" object (``.../js/submission_handler.js``), which handles the submission of results and all auditor data when the submit button is clicked.

Python
------
Similarly to the JavaScript side, the Python code (``.../survey/auditors.py``) across all auditors is rather similar and should be helpful when writing the models for your auditor. Firstly, add your auditor to the "NAME_TO_AUDITOR" dictionary at the top. You will then need to write a class for your auditor's data and for the auditor itself. The data class will have a "general_models" field with the foreign key being the name of your auditor and a field corresponding to each item specified in the auditor's returned object. For instance, if your auditor returned { 'count': some_int_var }, this class must have a "count" field that accepts data of type int. The actual auditor class has a "script_location" field, which is the directory and name of your auditor file, and a "data_model" field, which is simply the data class you just wrote.

Wrapping it Up
--------------
If the JavaScript and Python parts are implemented correctly, then your auditor should be able to save its data to the database correctly and without problems. You should be able to see and add your auditor to any new tasks you create, but be sure to test your code before publishing the task. It additionally might be helpful to write some unit tests for the auditor.

Documentation
=============
To add to or edit existing documentation, ``git checkout`` the ``sphinx`` branch. Make sure that your virtual environment is active. Source files are located in ``turkey/web/turkey/docs/source``. A ``Makefile`` is provided for convenience in the ``docs`` directory. To generate HTML files, simply run ``make html`` in the ``docs`` directory, and the build files will be located in ``build/html``. When you are finished working on documentation, you can make a `pull request <https://github.com/CuriousG102/turkey/pulls>`_ to the ``sphinx`` branch (not ``master``!).