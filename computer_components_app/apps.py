from django.apps import AppConfig


class ComputerComponentsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'computer_components_app'

    def ready(self):
        import computer_components_app.signals
