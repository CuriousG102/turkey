FROM python:3.5

RUN apt-get update && apt-get install -y libtiff5-dev libjpeg62-turbo-dev zlib1g-dev \
            libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk \
            postgresql-client openssl

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# this is an optimization if you put the RUN statement after the COPY of
# everything you will find yourself download all the dependencies every time
# you chagne any given file
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD ./setup.sh; cd turkey; python manage.py migrate; /usr/local/bin/gunicorn turkey.wsgi:application -c gunicorn_config.py