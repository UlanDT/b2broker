"""Module containing settings for tests."""

from .base import *

DEBUG = True
SECRET_KEY = env("DJANGO_SECRET_KEY", default="6K0MxSuQuSIEoiHMEg9QSxYVHFMnYmarCvUuZp9n7zKQG6AfkczcVetRB6BARfFx")
TEST_RUNNER = "django.test.runner.DiscoverRunner"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
