Overview and Inspiration
************************
Internal HITs on Amazon Mechanical Turk can be programmatically restrictive, and as a result, many requesters turn to using external HITs as a more flexible alternative. However, creating such HITs can be redundant and time-consuming. `MmmTurkey <https://github.com/CuriousG102/turkey/>`_ is a framework that enables researchers to not only quickly create and manage external HITs thanks to convenient built-in features, but more significantly also capture and record detailed worker behavioral data characterizing how each worker completes a given task. You can read out paper `here <https://arxiv.org/abs/1609.00945>`_.


Features
========
- More freedom to design a HIT
- No redundant code for every HIT created
- All tasks can be managed from a single, centralized dashboard
- Tasks automatically linked to a single Postgres database
- Response and auditor data for a HIT can be exported to XML
- Default auditors provided to gather data on worker interactions
    * Easy to add your own `custom auditor <extending.html#auditors>`_

- Default steps provided including multiple choice, text response, and checkbox selections
    * Easy to add your own `custom step <extending.html#steps>`_

