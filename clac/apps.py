from django.apps import AppConfig


class ClacConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clac"

    def ready(self):
        import clac.signals  # noqa: F401
