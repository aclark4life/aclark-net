from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class DBConfig(AppConfig):
    name = 'aclarknet.db'

    def ready(self):
        from .signals import login_receiver
        user_logged_in.connect(login_receiver)
