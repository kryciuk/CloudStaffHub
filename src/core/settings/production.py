from core.settings.common import *

env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = False
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_STATIC_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
RDS_DB_NAME = os.getenv("RDS_DB_NAME")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_HOSTNAME = os.getenv("RDS_HOSTNAME")
RDS_PORT = os.getenv("RDS_PORT")
SMTP_HOST = env("SMTP_HOST")
SMTP_PASSWORD = env("SMTP_PASSWORD")

ALLOWED_HOSTS = ("cloudstaffhub.eu-west-1.elasticbeanstalk.com",)

SECRET_KEY = env("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("RDS_DB_NAME"),
        "USER": os.getenv("RDS_USERNAME"),
        "PASSWORD": os.getenv("RDS_PASSWORD"),
        "HOST": os.getenv("RDS_HOSTNAME"),
        "PORT": os.getenv("RDS_PORT"),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("AWS_ACCESS_KEY_ID"),
            "secret_key": env("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": env("AWS_STORAGE_BUCKET_NAME"),
            "region_name": env("AWS_S3_REGION_NAME"),
            "file_overwrite": False,
        },
    },
    "PublicMediaStorage": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("AWS_ACCESS_KEY_ID"),
            "secret_key": env("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": env("AWS_STORAGE_BUCKET_NAME"),
            "region_name": env("AWS_S3_REGION_NAME"),
            "default_acl": "public-read",
            "location": "media/public",
            "querystring_auth": False,
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("AWS_ACCESS_KEY_ID"),
            "secret_key": env("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": env("AWS_STORAGE_BUCKET_NAME"),
            "region_name": env("AWS_S3_REGION_NAME"),
            "default_acl": "public-read",
            "location": "staticfiles",
            "querystring_auth": False,
        },
    },
}
