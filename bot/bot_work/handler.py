from bot.markup.markup import Keyboards
from bot.verification.user_verification import Verification
from business_logic.parse.parce_work import Parse_message
from db.db_work import DBManager
from business_logic.goal.goal_work import Goal
from business_logic.income.income_work import Income


class Handler:

    def __init__(self, bot):
        # получаем объект бота
        self.bot = bot
        # инициализируем разметку кнопок
        self.keybords = Keyboards()
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()
        # инициализируем работу с целями из БД
        self.goal = Goal()
        # инициализируем работу с доходами из БД
        self.income = Income()
        # инициализируем идентификации
        self.verification = Verification()
        # инициализируем файла для парсинга
        self.parse = Parse_message()

    def handle(self):
        pass
