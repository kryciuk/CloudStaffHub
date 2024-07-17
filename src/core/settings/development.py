from core.env import env
from core.settings.common import *

env.read_env(os.path.join(BASE_DIR, "../../.env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1 0.0.0.0:8000"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

SMTP_HOST = env("SMTP_HOST")
SMTP_PASSWORD = env("SMTP_PASSWORD")

MEDIA_ROOT = os.path.join(BASE_DIR.parent.parent, "src", "media")
