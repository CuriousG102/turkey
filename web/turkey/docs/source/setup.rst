Setup
*****

For Data Collection
===================
For data collection, we suggest you use a virtual server such as an Amazon EC2 instance or a DigitalOcean Droplet. Create and log into your server and install any necessary software packages. To use MmmTurkey, be sure to `install Docker and Docker Compose <https://docs.docker.com/compose/install>`_. The following commands will help guide you through the process of downloading and setting up MmmTurkey::

    git clone https://github.com/CuriousG102/turkey.git

    cd ./turkey

    export SECRET_KEY=your_arbitrary_secret_key
    docker-compose build
    docker-compose up

In a new terminal, you can type ``docker ps`` to view running Docker containers. Look for a container with a name along the lines of ``turkey_web_1`` (its image should be ``turkey_web``). To connect to and run commands in this container, run the following command::

    docker exec -i -t turkey_web_1 /bin/bash

MmmTurkey should now be ready to run locally for development on your machine. Navigate to `localhost <http://localhost/admin>`_ in your browser and you should hit the login page.

The above steps can be follows the next time you work on MmmTurkey, minus cloning the repository and creating and setting up the virtual environment. Creating a superuser (e.g., admin) really only needs to be done the first time you set up MmmTurkey::

    python manage.py createsuperuser

You will be prompted for your email address, a username, and a password. Once you have finished, you can then log in to the MmmTurkey dashboard in your browser using your credentials. The set up should then be complete. You are now free to `create new tasks <taskcreation.html>`_ or `view or export data <data.html>`_ for previous tasks if you have already created some.


For Local Development
=====================
For local development, it is best to avoid using Docker. It will make debugging harder, require you to use Postgres when you could use the lighter and easier to inspect SQLite3, and increase your time to iterate on code. Taking advantage of virtual environments, you can use the following commands within the project root directory to take a shortcut and speed up development (but first, be sure you have `Docker and Docker Compose installed <https://docs.docker.com/compose/install/>`_ ::

    git clone https://github.com/CuriousG102/turkey.git

    cd ./turkey/web

    virtualenv venv
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

    source venv/bin/activate

    export DEBUG=1
    docker-compose build
    docker-compose up

The remainder of this setup is identical to the above section. In a new terminal, you can type ``docker ps`` to view running Docker containers. Look for a container with a name along the lines of ``turkey_web_1`` (its image should be ``turkey_web``). To connect to and run commands in this container, run the following command::

    docker exec -i -t turkey_web_1 /bin/bash

MmmTurkey should now be ready to run locally for development on your machine. Navigate to `localhost <http://localhost/admin>`_ in your browser and you should hit the login page.

The above steps can be follows the next time you work on MmmTurkey, minus cloning the repository and creating and setting up the virtual environment. Creating a superuser (e.g., admin) really only needs to be done the first time you set up MmmTurkey::

    python manage.py createsuperuser

You will be prompted for your email address, a username, and a password. Once you have finished, you can then log in to the MmmTurkey dashboard in your browser using your credentials. The set up should then be complete. You are now free to `create new tasks <taskcreation.html>`_ or `view or export data <data.html>`_ for previous tasks if you have already created some.
