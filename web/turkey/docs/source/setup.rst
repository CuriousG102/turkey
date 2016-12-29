Setup
*****

For Data Collection
===================
For data collection, we suggest you use a virtual server such as an Amazon EC2 instance or a DigitalOcean Droplet. Create and log into your server and install any necessary software packages. To use MmmTurkey, be sure to `install Docker and Docker Compose <https://docs.docker.com/compose/install>`_. The following commands will help guide you through the process of downloading and setting up MmmTurkey::

    git clone https://github.com/CuriousG102/turkey.git

    cd ./turkey

    export SECRET_KEY=<your arbitrary secret key>
    export HOST=<your hostname or public DNS>
    
    service docker start
    docker-compose up

Note that you may be required to start docker as a root user. If this is the case, you must execute all subsequent docker commands as root as well. In a new terminal, you can type ``docker ps`` to view running Docker containers. Look for a container with a name along the lines of ``turkey_web_1`` (its image should be ``turkey_web``). To connect to and run commands in this container, run the following command::

    docker exec -i -t turkey_web_1 /bin/bash

MmmTurkey should now be ready and accessible via your web browser. Navigate to ``http://hostname/admin``, where ``hostname`` is the hostname of your instance, in your browser and you should reach the login page.

The above steps can be followed the next time you use MmmTurkey, minus cloning the repository. Creating a superuser (e.g., admin) only needs to be done the first time you set up MmmTurkey unless you later decide to add more admins::

    python manage.py createsuperuser

You will be prompted for your email address, a username, and a password. Once you have finished, you can then log in to the MmmTurkey dashboard in your browser using your credentials. The set up should then be complete. You are now free to `create new tasks <taskcreation.html>`_ or `view or export data <data.html>`_ for previous tasks if you have already created some.


For Local Development
=====================
For local development, we suggest the use of Docker and virtual environments. Once you have ``virtualenv`` and `Docker and Docker Compose installed <https://docs.docker.com/compose/install/>`_, the following commands will help guide you through the process of downloading and setting up MmmTurkey::

    git clone https://github.com/CuriousG102/turkey.git

    cd ./turkey/web

    virtualenv venv
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

    source venv/bin/activate

    export DEBUG=1

    service docker start
    docker-compose up

If you encounter failure when running ``pip install``, please refer to `this issue <https://github.com/CuriousG102/turkey/issues/53>`_. The remainder of this setup is identical to the above section. Note that you may be required to start docker as a root user. If this is the case, you must execute all subsequent docker commands as root as well. In a new terminal, you can type ``docker ps`` to view running Docker containers. Look for a container with a name along the lines of ``turkey_web_1`` (its image should be ``turkey_web``). To connect to and run commands in this container, run the following command::

    docker exec -i -t turkey_web_1 /bin/bash

MmmTurkey should now be ready to run locally for development on your machine. Navigate to `localhost <http://localhost/admin>`_ in your browser and you should reach the login page.

The above steps can be followed the next time you work on MmmTurkey, minus cloning the repository and creating and setting up the virtual environment. Creating a superuser (e.g., admin) only needs to be done the first time you set up MmmTurkey unless you later decide to add more admins::

    python manage.py createsuperuser

You will be prompted for your email address, a username, and a password. Once you have finished, you can then log in to the MmmTurkey dashboard in your browser using your credentials. The set up should then be complete. You are now free to work on MmmTurkey.
