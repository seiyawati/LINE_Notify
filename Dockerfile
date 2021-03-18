FROM python:3.6.6-stretch

ENV LANG C.UTF-8

WORKDIR /var/www/app
ADD requirements.txt /var/www/app/requirements.txt

RUN python3 -m pip install --upgrade pip \
        && python3 -m pip install -r /var/www/app/requirements.txt
ADD . /var/www/app
