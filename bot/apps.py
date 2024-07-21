from django.apps import AppConfig
from concurrent.futures import ProcessPoolExecutor

from . import bot


class BotConfig(AppConfig):
    name = 'bot'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        with ProcessPoolExecutor() as executor:
            executor.submit(bot.run)