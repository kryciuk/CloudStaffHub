from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "organizations"

    def ready(self):
        from organizations.signals import create_company_profile  # noqa: F401
