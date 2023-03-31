from django.core.management.base import BaseCommand
from bot.bot_work.core import TelBot


class Command(BaseCommand):

    help = 'Запускает пулинг телеграмм бота'

    def handle(self, *args, **options):
        print('Бот запущен')
        run_bot = TelBot()
        run_bot.start_handler()
        run_bot.run_bot()
