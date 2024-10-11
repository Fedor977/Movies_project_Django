from .base import *

ALLOWED_HOSTS = [
    '127.0.0.1'
]

SECRET_KEY = 'F8F98ERF89'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
# python manage.py runserver 0000
# http://127.0.0.1:8000 - default
# http://127.0.0.1:0000 - custom