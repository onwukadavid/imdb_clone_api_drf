from django.apps import AppConfig
from django.core.signals import request_finished

class UserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'
    
    def ready(self):
        from user_app import signals
        
        request_finished.connect(signals.create_auth_token)
