Setup
*****

For Data Collection
===================
For data collection, we suggest you use a virtual server such as an Amazon EC2 instance or a DigitalOcean Droplet. Create and log into your server and install any necessary software packages. To use MmmTurkey, be sure to `install Docker and Docker Compose <https://docs.docker.com/compose/install>`_. The following steps will help guide you through the process of downloading and setting up MmmTurkey.

First, clone and ``cd`` into the repo::

    git clone https://github.com/CuriousG102/turkey.git

    cd ./turkey

|
You will then need to set your ``SECRET_KEY`` (i.e., a password) and ``DOMAIN`` (i.e., the hostname or public DNS of your server) environment variables::

    export SECRET_KEY=<your arbitrary secret key>
    export DOMAIN=<your hostname or public DNS>

|
The next step is to start the Docker daemon and run the containers::
    
    service docker start
    docker-compose up

Note that you may be required to start Docker as a root user. If this is the case, you must execute all docker commands (including those above) as root and set your environment variables as root as well. If this is the case, it may be easiest to log into a root environment with ``sudo su`` before setting your environment variables in the previous step.
 
In a new terminal, you can type ``docker ps`` to view running Docker containers. Look for a container with a name along the lines of ``turkey_web_1`` (its image should be ``turkey_web``). To connect to and run commands in this container, run the following command, substituting ``turkey_web_1`` with the correct name of the container if necessary::

    docker exec -i -t turkey_web_1 /bin/bash


The above steps can be followed the next time you use MmmTurkey, minus cloning the repository. Creating a superuser (e.g., admin) only needs to be done the first time you set up MmmTurkey unless you need to add more admins::

    python manage.py createsuperuser

|
MmmTurkey should now be ready and accessible via your web browser. Navigate to ``http://hostname/admin``, where ``hostname`` is the hostname of your instance, in your browser and you should reach the login page. You can log into the dashboard using the credentials you just entered in.

You will be prompted for your email address, a username, and a password. Once you have finished, you can then log in to the MmmTurkey dashboard in your browser using your credentials. The setup should then be complete. You are now free to `create new tasks <taskcreation.html>`_ or `view or export data <data.html>`_ for previous tasks if you have already created some.


For Local Development
=====================
For local development, we suggest the use of Docker and virtual environments. Once you have the ``virtualenv`` package and `Docker and Docker Compose installed <https://docs.docker.com/compose/install/>`_, the following steps will help guide you through the process of downloading and setting up MmmTurkey.

First, clone and ``cd`` into the repo::

    git clone https://github.com/CuriousG102/turkey.git

    cd ./turkey/

|
Once you have ``virtualenv`` installed, you can run these commands to create, setup, and start your virtual environment::

    virtualenv venv
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r ./web/requirements.txt

    source venv/bin/activate

It is possible that you will need to install several other packages before running ``pip install``. If you encounter an error, please refer to `this issue <https://github.com/CuriousG102/turkey/issues/53>`_ for further instructions.

|
The following steps are for starting the server to view and test the framework::

    export DEBUG=1

    service docker start
    docker-compose up

|
In a new terminal, you can type ``docker ps`` to view running Docker containers. Look for a container with a name along the lines of ``turkey_web_1`` (its image should be ``turkey_web``). To connect to and run commands in this container, run the following command, substituting ``turkey_web_1`` with the correct name of the container if necessary::

    docker exec -i -t turkey_web_1 /bin/bash

|
The above steps can be followed the next time you work on MmmTurkey, minus cloning the repository and creating and setting up the virtual environment. Creating a superuser (e.g., admin) only needs to be done the first time you set up MmmTurkey unless you need to add more admins::

    python manage.py createsuperuser


MmmTurkey should now be ready to run locally for development on your machine. Navigate to `localhost <http://localhost/admin>`_ in your browser and you should reach the login page. You can log into the dashboard using the credentials you just entered in.

You will be prompted for your email address, a username, and a password. Once you have finished, you can then log in to the MmmTurkey dashboard in your browser using your credentials. The set up should then be complete. You are now free to work on MmmTurkey.
