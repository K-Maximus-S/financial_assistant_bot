from telegram.ext import CommandHandler
from bot.bot_work.handler import Handler


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start  и т.п.
    """

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, update, context):
        """
        Обрабатывает входящие /start команды.
        """
        update.message.reply_text(text='Привет', reply_markup=self.keybords.start_menu())

    def handle(self):
        self.bot.add_handler(CommandHandler('start', self.pressed_btn_start))
