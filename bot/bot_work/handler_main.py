from bot.bot_work.handler_com import HandlerCommands
from bot.bot_work.handler_all_text import HandlerAllText
from bot.bot_work.handler_FSM import HandlerFSM


class HandlerMain:
    """
    Класс компоновщик
    """

    def __init__(self, dp):
        self.dp = dp
        self.handler_commands = HandlerCommands(self.dp)
        self.handler_fsm = HandlerFSM(self.dp)
        self.handler_all_text = HandlerAllText(self.dp)

    def handle(self):
        # здесь будет запуск обработчиков
        self.handler_commands.handle()

        self.handler_fsm.handle_goal()
        self.handler_fsm.handle_edit_goal()
        self.handler_fsm.handle_income()
        self.handler_fsm.handle_edit_income()

        self.handler_all_text.handle()
