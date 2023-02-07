from django.apps import AppConfig


class App01Config(AppConfig):
    # id自动创建
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app01'
