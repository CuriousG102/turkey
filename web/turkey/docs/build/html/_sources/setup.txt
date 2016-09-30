Setup
*****

For Local Development
=====================
For local development it is best to avoid using Docker. It will make debugging harder, require you to use Postgres when you could use the lighter and easier to inspect SQLite3, and increase your time to iterate on code. You can use the following commands within web to take a shortcut and speed up development::

    virtualenv venv
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

    source venv/bin/activate

    cd /turkey/web/turkey
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

