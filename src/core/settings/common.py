import os
from pathlib import Path

from core.env import env

BASE_DIR = Path(__file__).resolve().parent.parent

X_FRAME_OPTIONS = "SAMEORIGIN"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    "widget_tweaks",
    "django_filters",
    "rest_framework",
    "django_extensions",
    "phonenumber_field",
    "bootstrap_datepicker_plus",
    "bootstrap4",
    "silk",
    "storages",
]

INSTALLED_EXTENSIONS = [
    "users",
    "recruitment",
    "evaluation",
    "recruiter",
    "organizations",
    "dashboards",
    "polls",
    "events",
    "owner",
    "landing",
]

INSTALLED_APPS += INSTALLED_EXTENSIONS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "core.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = "login"

MEDIA_URL = "/media/"

GROUPS_MANAGER = {
    "AUTH_MODELS_SYNC": True,
}

# SMTP Configuration

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# automatic logout

SESSION_COOKIE_AGE = 1000

SESSION_SAVE_EVERY_REQUEST = True

# phone number

PHONENUMBER_DEFAULT_REGION = "PL"

# datepicker

BOOTSTRAP_DATEPICKER_PLUS = {
    "options": {
        "locale": "en",
    },
    "variant_options": {
        "datetime": {
            "format": "DD.MM.YYYY HH:mm",
        },
    },
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
