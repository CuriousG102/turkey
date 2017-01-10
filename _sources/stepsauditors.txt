Steps and Auditors
******************

Steps
=====
If you think of your HIT as a test, then a "step" is an individual question in your test. You can add as many steps as you would like to your task, and you can choose to have them ordered or unordered (randomized). The same applies to the response options of each step, if applicable. The list of currently included steps is as follows:

- **Multiple Answer**: Checkbox question that allows the worker to select several answers.

- **Multiple Choice**: Classic multiple choice question that restricts the worker to selecting only one answer.

- **Text Input**: Question that requires the worker to type a textual response.

Auditors
========
Inspired by the `work <http://jeffrz.com/wp-content/uploads/2010/08/fp359-rzeszotarski.pdf>`_ of Jeff Rzeszotarski and Aniket Kittur, the framework provides "auditor" objects that record a worker's interactions with a task from the moment they start until they submit their responses or close out of the page. Auditor data can be used to analyze worker behavior and estimate the quality of responses. Doing this can potentially help identify bad response data or observe a behavioral pattern amongst workers. Auditors are written in JavaScript and primarily make use of jQuery events to detect browser interactions. Auditor code can be found in ``.../js/auditors``. Currently included auditors are as follows:

Focus-based Auditors
--------------------
Auditors recording whether the worker is on or off focus. A worker is considered on focus if the task page is "visible". The page is visible if it is not tabbed out, minimized, or closed. Primarily makes use of the `Page Visibility API <https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API>`_ to detect changes in focus.

- **Focus Changes**: Timestamps of whenever the worker switches out of focus (tabs out, minimizes, etc).

- **On Focus Time**: The total amount of time in milliseconds the worker spent on focus (not tabbed out, etc). Also a `Time-based Auditor <stepsauditors.html#time-based-auditors>`_.

- **Recorded Time Disparity**: The total amount of time in milliseconds the worker spent off focus (tabbed out, etc). Also a `Time-based Auditor <stepsauditors.html#time-based-auditors>`_.

Keyboard-based Auditors
-----------------------
Auditors recording typing interactions. Makes use of jQuery keyboard events.

- **Before Typing Delay**: Total time in milliseconds before a worker types; can be null.

- **Keypresses Total**: Total number of keypresses.

- **Keypresses Specific**: Keycode of the key that was pressed.

- **Within Typing Delay**: Checks if the worker typed within the first 10 seconds (default) of the task. Returns "true" if so, "false" if not.

Mouse-based Auditors
--------------------
Auditors recording mouse interactions. Makes use of jQuery's mousemove and click events. Additionally, makes use of `Ben Alman's jQuery debounce plugin <http://benalman.com/code/projects/jquery-throttle-debounce/examples/debounce/>`_.

- **Clicks Total**: Total number of times the worker clicks.

- **Clicks Specific**: The DOM element clicked by the worker. Reports the DOM type, id, class, and name.

- **Mouse Movement Total**: Total number of times the worker moves his mouse, debounced.

- **Mouse Movement Specific**: Ending position of the cursor after the worker moves his mouse, debounced.

Scroll-based Auditors
---------------------
Auditors recording scrolling events. Makes use of jQuery's scroll event and Ben Alman's jQuery debounce plugin.

- **Scrolled Pixels Total**: The total number of pixels scrolled by the worker. Returns both the vertical count and horizontal count, debounced.

- **Scrolled Pixels Specific**: For each scrolling event, reports the end position, the raw change in pixels from the previous position, and the timestamp of the event. Records data for both horizontal and vertical scrolling, debounced.

Time-based Auditors
-------------------
Auditors recording the time spent completing the task.

- **Total Task Time**: The total time it takes the worker to complete this task in milliseconds.

- **On Focus Time**: The total amount of time in milliseconds the worker spent on focus (not tabbed out, etc). Also a `Focus-based Auditor <stepsauditors.html#focus-based-auditors>`_.

- **Recorded Time Disparity**: The total amount of time in milliseconds the worker spent off focus (tabbed out, etc). Also a `Focus-based Auditor <stepsauditors.html#focus-based-auditors>`_.

Other Auditors
--------------
Pasting events, User Agent spying, and URL.

- **Pastes Total**: Total number of pastes actions.

- **Pastes Specific**: The content (text) of a paste action.

- **URL**: Returns the URL of the current page.

- **User Agent**: Returns the User Agent of the worker; can be parsed to find browser/version and operating system/version.