from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from bot.bot_work.handler import Handler
from bot.bot_work.handler_all_text import HandlerAllText
from business_logic.massage import MESSAGES


class Goal_list_id:
    """Структура целей для определенного пользователя из БД"""

    def __init__(self, number_goal_id, user_id_purposes_id, codename_id, category_id, aliases_id, price_id, data_id):
        self.number_goal_id = number_goal_id
        self.user_id_purposes_id = user_id_purposes_id
        self.codename_id = codename_id
        self.category_id = category_id
        self.aliases_id = aliases_id
        self.price_id = price_id
        self.data_id = data_id


class Income_list_id:
    """Структура доходов для определенного пользователя из БД"""

    def __init__(self, user_id_purposes_id, number_income_id, price_id, title_income_id):
        self.user_id_purposes_id = user_id_purposes_id
        self.number_income_id = number_income_id
        self.price_id = price_id
        self.title_income_id = title_income_id


class HandlerFSM(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от вода текста по системе FSM (конечный автомат)
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.handler_all_text = HandlerAllText(Handler)

        self.GOAL, self.CATEGORY, self.CODENAME, self.PRICE, self.DATAA, self.RESULT_GOAL = range(6)
        self.EDIT_CHOICE, self.EDIT_ALIASES, self.EDIT_CATEGORY, self.EDIT_CODENAME, self.EDIT_PRICE, self.EDIT_DATAA, self.EDIT_RESULT_GOAL, self.DEL_GOAL = range(
            8)
        self.EDIT_CHOICE_INCOME, self.EDIT_TITLE_INCOME, self.EDIT_PRICE_INCOME, self.EDIT_RESULT_INCOME, self.DEL_INCOME = range(
            5)
        self.PRICE_INCOME, self.RESULT_INCOME = range(2)

        self.edit_number = None
        self.edit_number_user_id_purposes = None
        self.edit_number_codename = None
        self.edit_number_category = None
        self.edit_number_aliases = None
        self.edit_number_price = None
        self.edit_number_data = None

        self.edit_number_user_id_purpose_income = None
        self.edit_number_income = None
        self.edit_number_price_income = None
        self.edit_number_title_income = None

        self.list_goal_id = []
        self.list_income_id = []

        self.list_goal_keyboard = []

    # =================================== Обработка постановки цели ========================================================

    def add_goal(self, update, context):
        update.message.reply_text("Вот так выглядит финансовая таблица:\n")
        update.message.reply_photo(open('table_fin.jpg', 'rb'))
        update.message.reply_text(MESSAGES['table_fin'], parse_mode='HTML')
        update.message.reply_text(
            "Если готов жми /goal\n"
            "Команда /cancel_goal, чтобы прекратить разговор.\n")
        return self.GOAL

    def goal_aliases(self, update, context):
        question = 'Как будет называться Цель'
        text_user = '.'
        example = 'Купить квартиру'
        update.message.reply_text(MESSAGES['pattern_goal'].format(question, text_user, example),
                                  parse_mode='HTML')

        user = update.message.reply_text(
            "Команда /cancel_goal, чтобы прекратить разговор.")
        return self.CATEGORY

    def category(self, update, context):
        context.user_data['key_goal'] = update.message.text
        user = update.message.from_user

        question = 'Какой категории будет относиться цель: '
        text_user = update.message.text
        example = 'Ипотека'
        update.message.reply_text(MESSAGES['pattern_goal'].format(question, text_user, example), parse_mode='HTML')

        user = update.message.reply_text("Команда /cancel_goal, чтобы прекратить разговор.")
        return self.CODENAME

    def codename(self, update, context):
        context.user_data['key_category'] = update.message.text

        question = 'Какому разделу будет относиться категория: '
        text_user = update.message.text
        example = 'Инвестиции'
        update.message.reply_text(MESSAGES['pattern_goal'].format(question, text_user, example), parse_mode='HTML')

        user = update.message.reply_text("Команда /cancel_goal, чтобы прекратить разговор.")
        return self.PRICE

    def price(self, update, context):
        context.user_data['key_codename'] = update.message.text

        question = 'Какая сумма цели: '
        text_user = update.message.text
        example = '5400500'
        update.message.reply_text(MESSAGES['pattern_goal'].format(question, text_user, example), parse_mode='HTML')

        user = update.message.reply_text("Команда /cancel_goal, чтобы прекратить разговор.")
        return self.DATAA

    def dataa(self, update, context):
        context.user_data['key_price'] = update.message.text

        question = 'Какая дата цели: '
        text_user = context.user_data['key_goal']
        example = '12.06.23'
        update.message.reply_text(MESSAGES['pattern_goal'].format(question, text_user, example), parse_mode='HTML')

        update.message.reply_text("Команда /cancel_goal, чтобы прекратить разговор.")
        return self.RESULT_GOAL

    def result_goal(self, update, context):
        context.user_data['key_data'] = update.message.text
        self.BD.insert_db_purposes(update.effective_user.id,
                                   context.user_data['key_codename'],
                                   context.user_data['key_category'],
                                   context.user_data['key_goal'],
                                   context.user_data['key_price'],
                                   context.user_data['key_data']
                                   )
        verification_result = self.verification.user_verification(update)
        self.verification.edit_verification(update, verification_result)
        update.message.reply_text(text='Вау! Цель поставлена!')
        self.handler_all_text.menu_finanse(update, context)
        return ConversationHandler.END

        # =================================== Редактирование целей ========================================================

    def edit_goal(self, update, context):
        number_goal_id = 0
        list_goal = self.goal.load_purposes()
        update.message.reply_text('Вот твои цели:\n'
                                  'Введи порядковый номер нужного дохода для редактирования или удаления')

        for goal in list_goal:
            user_id_purposes = int(goal.user_id_purposes)
            number_goal = goal.number_goal,
            aliases = goal.aliases,
            category = goal.category,
            codename = goal.codename
            price = goal.price,
            data = goal.data

            if update.message.from_user.id == user_id_purposes:
                number_goal_id += 1
                user_object = Goal_list_id(
                    user_id_purposes_id=user_id_purposes,
                    codename_id=codename,
                    category_id=category[0],
                    aliases_id=aliases[0],
                    price_id=price[0],
                    data_id=data,
                    number_goal_id=number_goal_id
                )
                self.list_goal_id.append(user_object)
                update.message.reply_text(MESSAGES['goal_list'].format(number_goal_id, aliases[0], price[0], data),
                                          parse_mode='HTML')
        update.message.reply_text("Команда /cancel_goal, чтобы прекратить разговор.")

        return self.EDIT_CHOICE

    def edit_choice(self, update, context):

        for goal_id in self.list_goal_id:
            user_id_purposes_id = goal_id.user_id_purposes_id,
            codename_id = goal_id.codename_id,
            category_id = goal_id.category_id,
            aliases_id = goal_id.aliases_id,
            price_id = goal_id.price_id,
            data_id = goal_id.data_id
            number_goal_id = goal_id.number_goal_id

            if int(update.message.text) == number_goal_id:
                self.edit_number_user_id_purposes = user_id_purposes_id[0]
                self.edit_number_codename = codename_id[0]
                self.edit_number_category = category_id[0]
                self.edit_number_aliases = aliases_id[0]
                self.edit_number_price = price_id[0]
                self.edit_number_data = data_id
                self.edit_number = number_goal_id
                break
            else:
                self.edit_number = False

        if self.edit_number == False:
            update.message.reply_text('Я не понял номер цели или цели с таким номером нет.\n'
                                      'Попробуй заново:\n\n')
            for goal_id in self.list_goal_id:
                user_id_purposes_id = goal_id.user_id_purposes_id,
                codename_id = goal_id.codename_id,
                category_id = goal_id.category_id,
                aliases_id = goal_id.aliases_id,
                price_id = goal_id.price_id,
                data_id = goal_id.data_id
                number_goal_id = goal_id.number_goal_id
                update.message.reply_text(
                    MESSAGES['goal_list'].format(number_goal_id, aliases_id[0], price_id[0], data_id),
                    parse_mode='HTML')
        else:
            update.message.reply_text("Твоя цель:")
            update.message.reply_text(
                MESSAGES['goal_list'].format(self.edit_number, self.edit_number_aliases, self.edit_number_price,
                                             self.edit_number_data), parse_mode='HTML')
            update.message.reply_text(f'Что с ней сделать ?\n'
                                      f'Команда /edit_aliases, чтобы изменить\n'
                                      f'Команда /del_goal, чтобы удалить\n'
                                      f'Команда /cancel_goal, чтобы прекратить разговор.')

            # edit_goal_def = self.EDIT_CATEGORY
        return self.EDIT_CHOICE

    def edit_aliases(self, update, context):
        update.message.reply_text(f'Приступим к изменению\n'
                                  f'Название цели: {self.edit_number_aliases}\n'
                                  f'1) Как будет называться Цель? (формат записи-> Купить машина или Ипотека)\n\n'
                                  f'Команда /cancel_goal, чтобы прекратить разговор.')
        return self.EDIT_CATEGORY

    def edit_category(self, update, context):
        context.user_data['key_egit_aliases'] = update.message.text
        user = update.message.from_user
        update.message.reply_text(f'Категория цели: {self.edit_number_category}\n'
                                  f'2) Какой категории будет относиться цель?:\n\n'
                                  f'Команда /cancel_goal, чтобы прекратить разговор.')
        return self.EDIT_CODENAME

    def edit_codename(self, update, context):
        context.user_data['key_egit_category'] = update.message.text
        update.message.reply_text(f'Раздел цели: {self.edit_number_aliases}\n'
                                  f'3) Какому разделу будет относиться цель ?:\n\n'
                                  f'Команда /cancel_goal, чтобы прекратить разговор.')
        return self.EDIT_PRICE

    def edit_price(self, update, context):
        context.user_data['key_edit_codename'] = update.message.text
        update.message.reply_text(f'Сумма цели: {self.edit_number_price}\n'
                                  f'4) Какая будет сумма цели?\n\n'
                                  f'Команда /cancel_goal, чтобы прекратить разговор.')
        return self.EDIT_DATAA

    def edit_dataa(self, update, context):
        context.user_data['key_edit_price'] = update.message.text
        update.message.reply_text(f'Дата цели: {self.edit_number_price}\n'
                                  f'5) Какая будет дата цели?\n\n'
                                  f'Команда /cancel_goal, чтобы прекратить разговор.')
        return self.EDIT_RESULT_GOAL

    def edit_result_goal(self, update, context):
        context.user_data['key_edit_data'] = update.message.text
        self.BD.delete_db_purposes(self.edit_number_user_id_purposes,
                                   self.edit_number_codename,
                                   self.edit_number_category,
                                   self.edit_number_aliases,
                                   self.edit_number_price,
                                   self.edit_number_data
                                   )

        self.BD.insert_db_purposes(update.effective_user.id,
                                   context.user_data['key_egit_aliases'],
                                   context.user_data['key_egit_category'],
                                   context.user_data['key_edit_codename'],
                                   context.user_data['key_edit_price'],
                                   context.user_data['key_edit_data']
                                   )
        self.list_goal_id.clear()

        update.message.reply_text(text='Вау! Цель изменилась!')
        verification_result = self.verification.user_verification(update)
        self.verification.edit_verification(update, verification_result)
        self.handler_all_text.menu_finanse(update, context)
        return ConversationHandler.END

    def del_goal(self, update, context):
        self.BD.delete_db_purposes(self.edit_number_user_id_purposes,
                                   self.edit_number_codename,
                                   self.edit_number_category,
                                   self.edit_number_aliases,
                                   self.edit_number_price,
                                   self.edit_number_data
                                   )
        self.list_goal_id.clear()

        update.message.reply_text(text='Вау! Цель удалена!')
        verification_result = self.verification.user_verification(update)
        self.verification.edit_verification(update, verification_result)
        self.handler_all_text.menu_finanse(update, context)
        return ConversationHandler.END

    # =================================== Обработка постановки дохода ======================================================

    def title_income(self, update, context):
        user = update.message.from_user
        user = update.message.reply_text(
            "1) Как будет называться доход ? (формат записи-> ЗП или соц.выплата)\n\n"
            "Команда /cancel_goal, чтобы прекратить разговор.")
        return self.PRICE_INCOME

    def price_income(self, update, context):
        user = update.message.from_user
        context.user_data['key_title_income'] = update.message.text
        user = update.message.reply_text(
            "2) Какая сумма дохода? ? (формат записи-> 50000)\n\n"
            "Команда /cancel_goal, чтобы прекратить разговор.")
        return self.RESULT_INCOME

    def result_income(self, update, context):
        context.user_data['key_price_income'] = update.message.text
        self.BD.insert_db_income(update.effective_user.id,
                                 context.user_data['key_price_income'],
                                 context.user_data['key_title_income']
                                 )
        verification_result = self.verification.user_verification(update)
        self.verification.edit_verification(update, verification_result)
        update.message.reply_text(text='Вау! Доход внесен!')
        self.handler_all_text.menu_finanse(update, context)
        return ConversationHandler.END

        # =================================== Редактирование доходов ========================================================

    def edit_income(self, update, context):
        number_income_id = 0
        list_income = self.income.load_income()
        update.message.reply_text('Список твоих доходов:\n'
                                  'Введи порядковый номер нужного дохода для редактирования')
        for income in list_income:
            user_id_purposes = int(income.user_id_purposes)
            number_goal = income.number_goal,
            price = income.price,
            title_income = income.title_income

            if update.message.from_user.id == user_id_purposes:
                number_income_id += 1
                user_object = Income_list_id(
                    user_id_purposes_id=user_id_purposes,
                    number_income_id=number_income_id,
                    price_id=price[0],
                    title_income_id=title_income
                )
                self.list_income_id.append(user_object)
                update.message.reply_text(MESSAGES['list_income'].format(number_income_id, title_income, price[0]),
                                          parse_mode='HTML')

        update.message.reply_text("Команда /cancel_goal, чтобы прекратить разговор.")
        return self.EDIT_CHOICE_INCOME

    def edit_choice_income(self, update, context):
        for income_id in self.list_income_id:
            user_id_purposes_id = income_id.user_id_purposes_id,
            price_id = income_id.price_id,
            title_income_id = income_id.title_income_id,
            number_goal_id = income_id.number_income_id

            if int(update.message.text) == number_goal_id:
                self.edit_number_user_id_purpose_income = user_id_purposes_id[0]
                self.edit_number_income = number_goal_id
                self.edit_number_price_income = price_id[0]
                self.edit_number_title_income = title_income_id[0]
                break
            else:
                self.edit_number_income = False

        if self.edit_number_income == False:
            update.message.reply_text('Я не понял номер дохода или дохода с таким номером нет.\n'
                                      'Попробуй заново:\n\n')
            for income_id in self.list_income_id:
                user_id_purposes_id = income_id.user_id_purposes,
                number_goal_id = income_id.number_income_id,
                price_id = income_id.price[0],
                title_income_id = income_id.title_income
                update.message.reply_text(MESSAGES['list_income'].format(number_goal_id, title_income_id, price_id[0]),
                                          parse_mode='HTML')
        else:
            update.message.reply_text("Твой доход:")
            update.message.reply_text(
                MESSAGES['list_income'].format(self.edit_number_income, self.edit_number_title_income,
                                               self.edit_number_price_income),
                parse_mode='HTML')
            update.message.reply_text(f'Что с ней сделать ?\n'
                                      f'Команда /edit_title_income, чтобы изменить\n'
                                      f'Команда /del_income, чтобы удалить\n'
                                      f'Команда /cancel_goal, чтобы прекратить разговор.')
        return self.EDIT_CHOICE_INCOME

    def edit_title_income(self, update, context):
        update.message.reply_text(f'Приступим к изменению\n'
                                  f'Название цели: {self.edit_number_title_income}\n'
                                  f'1) Как будет называться Доход? (формат записи-> Зп или Соц.выплата)\n\n'
                                  f'Команда /cancel_goal, чтобы прекратить разговор.')
        return self.EDIT_PRICE_INCOME

    def edit_price_income(self, update, context):
        context.user_data['key_egit_title_income'] = update.message.text
        user = update.message.from_user
        update.message.reply_text(f'Сумма дохода: {self.edit_number_price_income}\n'
                                  f'2) Какая сумма дохода?:\n\n'
                                  f'Команда /cancel_goal, чтобы прекратить разговор.')
        return self.EDIT_RESULT_INCOME

    def edit_result_income(self, update, context):
        context.user_data['key_egit_price_income'] = update.message.text
        self.BD.delete_db_income(self.edit_number_user_id_purpose_income,
                                 self.edit_number_price_income,
                                 self.edit_number_title_income
                                 )

        self.BD.insert_db_income(update.effective_user.id,
                                 context.user_data['key_egit_price_income'],
                                 context.user_data['key_egit_title_income']
                                 )
        self.list_income_id.clear()

        update.message.reply_text(text='Вау! Доход изменился!')
        verification_result = self.verification.user_verification(update)
        self.verification.edit_verification(update, verification_result)
        self.handler_all_text.menu_finanse(update, context)
        return ConversationHandler.END

    def del_income(self, update, context):
        self.BD.delete_db_income(self.edit_number_user_id_purpose_income,
                                 self.edit_number_price_income,
                                 self.edit_number_title_income
                                 )
        self.list_goal_id.clear()

        update.message.reply_text(text='Вау! Доход удален!')
        verification_result = self.verification.user_verification(update)
        self.verification.edit_verification(update, verification_result)

        self.handler_all_text.menu_finanse(update, context)
        return ConversationHandler.END

    # =================================== Обработка выхода из FSM ========================================================

    def cancel_goal(self, update, context):
        user = update.message.from_user
        self.handler_all_text.menu_finanse(update, context)
        # update.message.reply_text(text='Вы вернулись назад', reply_markup=self.keybords.start_menu())
        return ConversationHandler.END

    # =================================== Обработка по FSM ===============================================================

    # ------------- Обработка цели ---------

    def handle_goal(self):
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text('Add_goal'), callback=self.add_goal)],
            states={
                self.GOAL: [CommandHandler('cancel_goal', self.cancel_goal),
                            MessageHandler(Filters.text, self.goal_aliases)],
                self.CATEGORY: [CommandHandler('cancel_goal', self.cancel_goal),
                                MessageHandler(Filters.text, self.category)],
                self.CODENAME: [CommandHandler('cancel_goal', self.cancel_goal),
                                MessageHandler(Filters.text, self.codename)],
                self.PRICE: [CommandHandler('cancel_goal', self.cancel_goal),
                             MessageHandler(Filters.text, self.price)],
                self.DATAA: [CommandHandler('cancel_goal', self.cancel_goal),
                             MessageHandler(Filters.text, self.dataa)],
                self.RESULT_GOAL: [CommandHandler('cancel_goal', self.cancel_goal),
                                   MessageHandler(Filters.text, self.result_goal)]
            },
            fallbacks=[CommandHandler('cancel_goal', self.cancel_goal)],
        )
        self.bot.add_handler(conv_handler)

        return

    # ------------- Обработка редактирования цели ---------

    def handle_edit_goal(self):
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text('Edit_goal'), callback=self.edit_goal)],
            states={
                self.EDIT_CHOICE: [CommandHandler('cancel_goal', self.cancel_goal),
                                   CommandHandler('del_goal', self.del_goal),
                                   CommandHandler('edit_aliases', self.edit_aliases),
                                   MessageHandler(Filters.text, self.edit_choice)],
                self.EDIT_ALIASES: [CommandHandler('cancel_goal', self.cancel_goal),
                                    MessageHandler(Filters.text, self.edit_aliases)],
                self.EDIT_CATEGORY: [CommandHandler('cancel_goal', self.cancel_goal),
                                     MessageHandler(Filters.text, self.edit_category)],
                self.EDIT_CODENAME: [CommandHandler('cancel_goal', self.cancel_goal),
                                     MessageHandler(Filters.text, self.edit_codename)],
                self.EDIT_PRICE: [CommandHandler('cancel_goal', self.cancel_goal),
                                  MessageHandler(Filters.text, self.edit_price)],
                self.EDIT_DATAA: [CommandHandler('cancel_goal', self.cancel_goal),
                                  MessageHandler(Filters.text, self.edit_dataa)],
                self.EDIT_RESULT_GOAL: [CommandHandler('cancel_goal', self.cancel_goal),
                                        MessageHandler(Filters.text, self.edit_result_goal)],
                self.DEL_GOAL: [CommandHandler('cancel_goal', self.cancel_goal),
                                MessageHandler(Filters.text, self.del_goal)]
            },
            fallbacks=[CommandHandler('cancel_goal', self.cancel_goal)],
        )
        self.bot.add_handler(conv_handler)

    # ------------- Обработка доходов ---------
    def handle_income(self):
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text('Add_income'), callback=self.title_income)],
            states={
                self.PRICE_INCOME: [CommandHandler('cancel_goal', self.cancel_goal),
                                    MessageHandler(Filters.text, self.price_income)],
                self.RESULT_INCOME: [CommandHandler('cancel_goal', self.cancel_goal),
                                     MessageHandler(Filters.text, self.result_income)]
            },
            fallbacks=[CommandHandler('cancel_goal', self.cancel_goal)],
        )
        self.bot.add_handler(conv_handler)

    # ------------- Обработка редактирования дохода ---------

    def handle_edit_income(self):
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text('Edit_income'), callback=self.edit_income)],
            states={
                self.EDIT_CHOICE_INCOME: [CommandHandler('cancel_goal', self.cancel_goal),
                                          CommandHandler('del_income', self.del_income),
                                          CommandHandler('edit_title_income', self.edit_title_income),
                                          MessageHandler(Filters.text, self.edit_choice_income)],
                self.EDIT_TITLE_INCOME: [CommandHandler('cancel_goal', self.cancel_goal),
                                         MessageHandler(Filters.text, self.edit_title_income)],
                self.EDIT_PRICE_INCOME: [CommandHandler('cancel_goal', self.cancel_goal),
                                         MessageHandler(Filters.text, self.edit_price_income)],
                self.EDIT_RESULT_INCOME: [CommandHandler('cancel_goal', self.cancel_goal),
                                          MessageHandler(Filters.text, self.edit_result_income)],
                self.DEL_INCOME: [CommandHandler('cancel_goal', self.cancel_goal),
                                  MessageHandler(Filters.text, self.del_income)]
            },
            fallbacks=[CommandHandler('cancel_goal', self.cancel_goal)],
        )
        self.bot.add_handler(conv_handler)
