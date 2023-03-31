from bot.bot_work.handler import Handler
from telegram.ext import MessageHandler, Filters
from business_logic.massage import MESSAGES


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)

    def menu_finanse(self, update, context):
        """
        Обрабатывает входящие текстовые сообщения
        от нажатия на кнопоку 'Финансы'.
        """
        verification_result = self.verification.user_verification(update)
        if verification_result == 1:
            update.message.reply_text(text='Для работы с финансами необходимо поставить цели:\n'
                                           '1. Поставить цели -> Кнопка Add_goal\n',
                                      reply_markup=self.keybords.menu_fin_1())
        elif verification_result == 2:
            update.message.reply_text(text='Для работы с финансами необходимо внести доходы за месяц:\n'
                                           '1. Внести доходы -> Кнопка Add_income\n',
                                      reply_markup=self.keybords.menu_fin_2())
        elif verification_result == 3:
            update.message.reply_text(text='У тебя есть доходы, но увы нет целей(\n'
                                           'Давай это исправим\n'
                                           '1. Внести Цель -> Кнопка Add_goal\n',
                                      reply_markup=self.keybords.menu_fin_1())
        elif verification_result == 4:
            update.message.reply_text(text='Основное меню\n\n'
                                           'Работа с целями:\n'
                                           '1. Посмотреть цели -> Кнопка List_goal \n'
                                           '2. Изменить цели -> Кнопка Edit_goal\n'
                                           '3. Поставить цели -> Кнопка Add_goal\n\n'
                                           'Работа с доходами:\n'
                                           '4. Посмотреть доходы -> Кнопка List_income\n'
                                           '5. Изменить доходы -> Кнопка Edit_income\n'
                                           '6. Добавить доходы -> Кнопка Add_income\n\n'
                                           'Если все Ок! Переходи к работе с расходами\n'
                                           '7. Добавить расход -> Введи текс\n'
                                           '(Формат 200 1 Еда)\n'
                                           'Где: 200 - цена,\n'
                                           '1 - количество,\n'
                                           'Еда - Цель(расход)\n'
                                           'Необходимо соблюдать пробелы!!!!',
                                      reply_markup=self.keybords.menu_fin_3()) # TODO: Доделать нормальный вод,
        elif verification_result == 5:
            update.message.reply_text(text='Для работы с финансами необходимо поставить цели:\n'
                                           '1. Поставить цели -> Кнопка Add_goal\n',
                                      reply_markup=self.keybords.menu_fin_1())

    def menu_info(self, update, context):
        """
        Обрабатывает входящие текстовые сообщения
        от нажатия на кнопоку 'О проекте'.
        """
        # update.message.text
        update.message.reply_text(MESSAGES['trading_store'],
                                  parse_mode='HTML',
                                  reply_markup=self.keybords.info_menu())  # TODO: Ответ должен быть но id пользователя

    def menu_settings(self, update, context):
        """
        Обрабатывает входящие текстовые сообщения
        от нажатия на кнопоку 'Настройки'.
        """
        update.message.reply_text(MESSAGES['settings'],
                                  parse_mode='HTML',
                                  reply_markup=self.keybords.settings_menu())  # TODO: Ответ должен быть но id пользователя

    def menu_back(self, update, context):
        """
        обрабатывает входящие текстовые сообщения
        от нажатия на кнопку 'Назад'.
        """
        update.message.reply_text(text="Вы вернулись назад",
                                  reply_markup=self.keybords.start_menu())

    def list_goal(self, update, context):
        """Получение списка целей из БД"""
        number_goal_id = 0
        list_goal = self.goal.load_purposes()
        update.message.reply_text('Вот твои цели:\n')
        for goal in list_goal:
            user_id_purposes = int(goal.user_id_purposes)
            aliases = goal.aliases,
            price = goal.price,
            data = goal.data

            if update.message.from_user.id == user_id_purposes:
                number_goal_id += 1
                update.message.reply_text(MESSAGES['goal_list'].format(number_goal_id, aliases[0], price[0], data),
                                          parse_mode='HTML')

        self.menu_finanse(update, context)

    def list_income(self, update, context):
        """Получение списка доходов из БД"""
        number_goal_id = 0
        list_income = self.income.load_income()
        update.message.reply_text('Вот твои доходы:\n')
        for income in list_income:
            user_id_purposes = int(income.user_id_purposes),
            price = income.price,
            title_income = income.title_income

            if update.message.from_user.id == user_id_purposes[0]:
                number_goal_id += 1
                update.message.reply_text(MESSAGES['list_income'].format(number_goal_id, title_income, price[0]),
                                          parse_mode='HTML')

        self.menu_finanse(update, context)

    def add_expense(self, update, context):
        """Добавление нового расхода в БД"""

        for palse_user in self.parse.list_from_message(update):
            aliases = palse_user.alias,
            price = palse_user.price,
            quantity = palse_user.quantity,
            raw_text = palse_user.raw_text

            self.BD.insert_db_expenses_needs(user_id_purposes=update.message.from_user.id,
                                             codename='None',
                                             category='None',
                                             aliases=aliases[0],
                                             price=price[0],
                                             quantity=quantity[0],
                                             raw_text=raw_text
                                             )
            update.message.reply_text(f"Добавлены траты {price[0]} руб на {aliases[0]}.")
            self.parse.list_parse.clear()
            self.menu_finanse(update, context)

    def handle(self):
        """
        Обрабатывает входящие текстовые сообщения
        от нажатия кнопок.
        """
        # ============ Обработка команды финансы после start_menu ==========
        self.bot.add_handler(MessageHandler(Filters.text('📑 Финансы'), callback=self.menu_finanse))
        self.bot.add_handler(MessageHandler(Filters.text('⚙️ Настройки'), callback=self.menu_settings))
        self.bot.add_handler(MessageHandler(Filters.text('💬 О проекте'), callback=self.menu_info))

        self.bot.add_handler(MessageHandler(Filters.text('List_goal'), callback=self.list_goal))
        self.bot.add_handler(MessageHandler(Filters.text('List_income'), callback=self.list_income))

        self.bot.add_handler(MessageHandler(Filters.text('⏪'), callback=self.menu_back))
        self.bot.add_handler(MessageHandler(Filters.text, callback=self.add_expense))
