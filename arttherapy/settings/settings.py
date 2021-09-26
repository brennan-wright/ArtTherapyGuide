import os
import socket

import dj_database_url
import requests
from requests.exceptions import ConnectionError

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
DEBUG = int(os.environ.get("DEBUG"))
SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

url = "http://169.254.169.254/latest/meta-data/local-ipv4"
# try:
#     r = requests.get(url)
#     instance_ip = r.text
#     ALLOWED_HOSTS += [instance_ip]
# except ConnectionError:
#     error_msg = "You can only run production settings on an AWS EC2 instance"
#     raise ConnectionError(error_msg)


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'debug_toolbar',
    "frontend",
    "directive",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'captcha',
    'widget_tweaks',
    'storages',
]

SITE_ID = 1

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

ROOT_URLCONF = "arttherapy.urls"

ADMINS = [('ADMIN', os.environ.get("ADMIN_EMAIL")), ]
MANAGERS = ADMINS

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates"), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "arttherapy.wsgi.application"


# Database
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"], conn_max_age=600
    )
}


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Authentication Settings
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_BLACKLIST = ["admin", "god"]
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_FORMS = {'signup': 'users.forms.CustomSignupForm'}


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]


# Email Settings
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")


# Static Files Settings
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/static"),
]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"


# Media Files Settings
if not DEBUG:
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"


# Recaptcha Settings
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
RECAPTCHA_REQUIRED_SCORE = 0.85
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
