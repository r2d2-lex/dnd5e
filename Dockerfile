FROM python:3.7-alpine

WORKDIR /xardas

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN pip install -r requirements.txt

COPY ./xardas .

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
