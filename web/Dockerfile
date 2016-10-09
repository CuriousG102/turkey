FROM python:3.5

RUN apt-get update && apt-get install -y libtiff5-dev libjpeg62-turbo-dev zlib1g-dev \
            libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk \
            postgresql-client

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ./setup.sh; cd turkey; python manage.py migrate; /usr/local/bin/gunicorn turkey.wsgi:application -c gunicorn_config.py