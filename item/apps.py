from django.apps import AppConfig

class ItemConfig(AppConfig):
    # Specifies the default auto field to use when creating models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    # Name of the Django app
    name = 'item'
