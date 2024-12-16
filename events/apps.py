from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'


class EventAppConfig(AppConfig):
    name = 'events'

    def ready(self):
        import events.signals