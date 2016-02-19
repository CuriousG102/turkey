FROM python:3.4

RUN apt-get update && apt-get install -y libtiff5-dev libjpeg62-turbo-dev zlib1g-dev \
            libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
