FROM python:3.7-alpine

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

WORKDIR /ksardas

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers

RUN pip install -r requirements.txt

COPY ./ksardas .

# EXPOSE 8000
#
# # RUN python manage.py makemigrations
# # RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
