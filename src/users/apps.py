from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from users.signals import create_profile, populate_models
        post_migrate.connect(populate_models, sender=self)
