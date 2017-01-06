Using Data
**********
For a created task, the following are stored in a Postgres database: the metadata of the task, worker responses, metadata for each response, and auditor data for a response. Data stored in the database can be exported to XML. To view the XML, navigate to ``<your_site>/admin/survey/task/``. Select the tasks for which you would like to retrieve responses, select the "Export tasks data" action, and hit "Go". Parse away.

Additionally, you can view and manipulate task data in Jupyter iPython notebooks.
.. todo: tutorial