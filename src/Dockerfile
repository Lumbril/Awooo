FROM python:3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . ./src

CMD gunicorn --chdir ./src Awooo.wsgi:application --bind 0.0.0.0:8000
CMD python3 src/manage.py migrate
CMD python3 src/manage.py collectstatic --noinput
