from django.apps import AppConfig

class MainConfig(AppConfig):
    name = 'main'  # your app name

    def ready(self):
        import main.signals  # ⚠️ Make sure this matches your app name
