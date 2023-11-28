from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = "djfritz"
    verbose_name = "DjFritz"

    def ready(self):
        import djfritz.signals  # noqa
