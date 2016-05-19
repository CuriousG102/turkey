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

Add your step to the dictionary `NAME_TO_STEP` at the top of the file. You will need to write two classes,
one for the step's data and one for the step itself. The data class will have a "general_models" field with
the foreign key being the name of your step and a "response" field specifying the type of response your database
should expect to receive (int, text, etc). The step class has a "script_location" field, a "template_file"
location field, a "data_model" field (which is simply the data class you just wrote), and some metadata fields
specific to an instance of this step such as "title" and "text" (question text). Fields in this class will affect
how the process of adding this step will appear on the admin site. Note that a step's fields can be accessed in a
template with step_instance.attribute; this can be helpful when filling out HTML element fields.Sp

Javascript
++++++++++
Scripts are located in (.../js/steps/). Create an object with a `submit_callable` function that returns an object.
This object should get the responses of every instance of this specific step type, and each instance's response
should be paired with its primary key in the return object. jQuery should be extremely helpful in extracting the
responses of a step instance. After writing this object, be sure to register your step to the "overlord" object
(.../js/submission_handler.js), which handles the submission of results and all auditor data when the submit button
is clicked.

Auditors
========
Models for auditors are in

Inspired by the work of
`Jeff Rzeszotarski and Aniket Kittur <http://jeffrz.com/wp-content/uploads/2010/08/fp359-rzeszotarski.pdf>`_, the
framework provides auditors objects that record a worker's interactions with a task from the moment they start until
they submits their responses or closes out of the page. Auditor data can be used to analyze the merit of a worker
and estimate the quality of their responses. Doing this can help filter out bad response data and potentially identify
workers who repeatedly provide poor quality work as well as detect a pattern amongst workers with varying levels of
work ethic. Auditors are written in JavaScript (.../js/auditors/) and primarily make use of jQuery events to detect
browser interactions.

Currently Included Auditors
---------------------------
Focus Based Auditors
++++++++++++++++++++
Auditors recording whether the worker is on or off focus. A worker is considered on focus if the task page is "visible".
The page is visible if it is not tabbed out, minimized, or closed. Primarily makes use of the Page Visibility API
(.../js/globals/visbility_changes) to detect changes in focus.

Focus Changes
+++++++++++++
Timestamps of whenever the worker switches out of focus (tabs out, minimizes, etc).

On Focus Time
+++++++++++++
The total amount of time in milliseconds the worker spent on focus (not tabbed out, etc).

Recorded Time Disparity
+++++++++++++++++++++++
The total amount of time in milliseconds the worker spent off focus (tabbed out, etc). Also a Time Based Auditor

Keyboard Based Auditors
+++++++++++++++++++++++
Auditors recording typing interactions. Makes use of jQuery keyboard events.

Before Typing Delay
+++++++++++++++++++
Total time in milliseconds before a worker types; can be null.

Keypresses Total
++++++++++++++++
Total number of keypresses

Keypresses Specific
+++++++++++++++++++
Keycode of the key that was pressed.

Within Typing Delay
+++++++++++++++++++
Checks if the worker typed within the first 10 (default) seconds of the task. Returns "true" if so, "false" if not.

Mouse Based Auditors
++++++++++++++++++++
Auditors recording mouse interactions. Makes use of jQuery's mousemove and click events.

Clicks Total
++++++++++++
Total number of times the worker clicks.

Clicks Specific
+++++++++++++++
The DOM element clicked by the worker. Reports the DOM type, id, class, and name.

Mouse Movement Total
++++++++++++++++++++
Total number of times the worker moves his mouse, debounced.

Mouse Movement Specific
+++++++++++++++++++++++
Ending position of the cursor after the worker moves his mouse, debounced.

Scroll Base Auditors
++++++++++++++++++++
Auditors recording scrolling events. Makes use of jQuery's scroll event and the jQuery debounce plugin
(.../js/globals/jquery.ba-throttle-debounce.min.js).

Scrolled Pixels Total
+++++++++++++++++++++
The total number of pixels scrolled by the worker. Returns both the vertical count and horizontal count. Debounced.

Scrolled Pixels Specific
++++++++++++++++++++++++
For each scrolling event, reports the end position, the raw change in pixels from the previous position, and the
timestamp of the event. Records data for both horizontal and vertical scrolling. Debounced.

Time Based Auditors
+++++++++++++++++++
Auditors recording the time spent completing the task.

Total Task Time
+++++++++++++++
The total time it takes the worker to complete this task in milliseconds.

Recorded Time Disparity
+++++++++++++++++++++++
The total amount of time in milliseconds the worker spent off focus (tabbed out, etc). Also a Focus Based Auditor

Other Auditors
++++++++++++++
Pasting events and User Agent spying.

Pastes Total
++++++++++++
Total number of pastes actions.

Pastes Specific
+++++++++++++++
The content (text) of a paste action.

User Agent
++++++++++
Returns the User Agent of the worker; can be parsed to find browser/version and operating system/version.

Writing Your Own
----------------
Javascript: The Actual Auditor
++++++++++++++++++++++++++++++
Auditors generally have the same format, and referencing the default auditors can be helpful when trying
to write your own. Create a JavaScript auditor object (.../js/auditors/) with your needed fields, a function that
modifies those fields, and a function to submit those fields. The modifier function is the action that should be
executed when your auditor detects a certain interaction. The submission function ("submit_callable") must return a
JavaScript object or array of JavaScript objects. The fields can have the value of a single value (int, string, etc).
Be sure to register your auditor to the "overlord" object (.../js/submission_handler.js), which handles the submission
of results and all auditor data when the submit button is clicked.

Python: The Auditor's Models
++++++++++++++++++++++++++++
Similarly to the JavaScript side, the Python code (.../survey/auditors.py) across all auditors is rather similar and
should be helpful when writing the models for your auditor. Firstly, add your auditor to the "NAME_TO_AUDITOR"
dictionary at the top. You will then need to write a class for your auditor's data and for the auditor itself.
The data class will have a "general_models" field with the foreign key being the name of your auditor and a field
corresponding to each item specified in the auditor's returned object. For instance, if your auditor returned
{ 'count': some_int_var }, this class must have a "count" field that accepts data of type int. The actual auditor class
has a "script_location" field, which is the directory and name of your auditor file, and a "data_model" field, which is
simply the data class you just wrote.

Wrapping it Up
++++++++++++++
If the JavaScript and Python parts were implemented correctly, then your auditor should be able to save its data to the
database correctly and without problems. You should be able to see and add your auditor to any new tasks you create, but
be sure to test your code before publishing the HIT.
