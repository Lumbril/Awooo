import os

from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('HOST'),
    }
}