"""
A standalone test runner script, configuring the minimum settings
required for tests to execute.

Re-use at your own risk: many Django applications will require
different settings and/or templates to run their tests.

"""

import os
import sys


# Make sure the app is (at least temporarily) on the import path.
APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, APP_DIR)


# Minimum settings required for the app's tests.
SETTINGS_DICT = {
    "BASE_DIR": APP_DIR,
    "INSTALLED_APPS": (
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "uaa_client",
    ),
    # Test cases will override this liberally.
    "ROOT_URLCONF": "uaa_client.tests.urls",
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(APP_DIR, "db.sqlite3"),
        }
    },
    "AUTHENTICATION_BACKENDS": ["uaa_client.authentication.UaaBackend"],
    "MIDDLEWARE_CLASSES": (
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ),
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(APP_DIR, "tests/templates")],
            "APP_DIRS": True,
            "OPTIONS": {"context_processors": []},
        }
    ],
    "UAA_CLIENT_ID": "something",
    "UAA_CLIENT_SECRET": "something_secret",
    "UAA_AUTH_URL": "https://auth.example.gov",
    "UAA_TOKEN_URL": "https://token.example.gov",
    "SECRET_KEY": "only-for-testing",
}

# Django 2.0+
SETTINGS_DICT["MIDDLEWARE"] = SETTINGS_DICT["MIDDLEWARE_CLASSES"]


def run_tests():
    # Making Django run this way is a two-step process. First, call
    # settings.configure() to give Django settings to work with:
    from django.conf import settings

    settings.configure(**SETTINGS_DICT)

    # Then, call django.setup() to initialize the application cache
    # and other bits:
    import django

    if hasattr(django, "setup"):
        django.setup()

    # Now we instantiate a test runner...
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)

    # And then we run tests and return the results.
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(["uaa_client.tests"])
    sys.exit(bool(failures))


if __name__ == "__main__":  # pragma: no cover
    run_tests()  # pragma: no cover
