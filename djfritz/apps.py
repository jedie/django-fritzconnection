from django.apps import AppConfig


class DjFritzConfig(AppConfig):
    name = "djfritz"
    verbose_name = "DjFritz"

    def ready(self):
        import djfritz.signals  # noqa
