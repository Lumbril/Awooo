FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . ./src

WORKDIR /app/src

CMD python manage.py collectstatic --no-input && \
    python manage.py migrate --no-input && \
    python manage.py createsuperuser --email "$DJANGO_SUPERUSER_EMAIL" --no-input || true && \
    daphne -b 0.0.0.0 -p 8000 Awooo.asgi:application
