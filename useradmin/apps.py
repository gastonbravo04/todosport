from django.apps import AppConfig

class UseradminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'useradmin'
    def ready(self):
        from . import signals  # noqa
