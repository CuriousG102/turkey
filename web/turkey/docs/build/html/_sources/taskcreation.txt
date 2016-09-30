Creating a Task
***************

At the admin home, select "Add interactive task". A new task requires an owner and a title. Hit "Save and continue editing" before adding steps or auditors.

Steps
=====
Simply put, a `step <extending.html#steps>`_ is a question or interaction in the HIT. A step can be a multiple choice question, text response, checkbox question, or a custom interaction written by a requester. A task can have any number of steps, either in a specified order or a randomized order.

Auditors
========
Inspired by the work of `Jeff Rzeszotarski and Aniket Kittur <http://jeffrz.com/wp-content/uploads/2010/08/fp359-rzeszotarski.pdf>`_

`Auditors <extending.html#auditors>`_ act as spies that record a worker's interactions while working on a HIT. Information such as what the user is clicking or typing, the position of his mouse at a certain time, or how often he tabs out is recorded and stored in the database. Information about a worker's interactions can be used to judge the merit of a worker and filter out repeated "bad" workers/responses in future HITs. Any number of auditors can be added to a task, but only one instance of each is allowed to be added.

Note that data recording begins whenever a worker starts working on a HIT rather than just sending all the information when the submit button is clicked. Tasks cannot be modified after data recording begins; this includes modifying the task name, adding more steps or auditors, or modifying a step's text prompt.