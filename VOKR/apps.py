from django.apps import AppConfig

class VOKRConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'VOKR'
    label = 'vokr_app'

    def ready(self):
        from .core.singleton import WSLProcessSingleton
        WSLProcessSingleton()
