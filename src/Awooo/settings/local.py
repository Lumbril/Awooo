import os

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
