from telegram import KeyboardButton, ReplyKeyboardMarkup
from business_logic import config


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """

    def __init__(self):
        self.markup = None

    def set_btn(self, name):
        """
        Создает и возвращает кнопку по входным параметрам
        """
        keyboard_menu = [
            [KeyboardButton(f"{config.KEYBOARD[ist]}") for ist in name]
        ]
        return keyboard_menu

    # # ================== Шаблон для инлайн кнопки ====================================================
    #
    # def set_btn_inline(self, var):
    #     """
    #     Создает и возвращает инлайн кнопку по входным параметрам
    #     """
    #     return_inline = [
    #         [
    #             InlineKeyboardButton(f"{ss}", callback_data=self.EDIT_CHOICE)for ss in var
    #         ]
    #     ]
    #     return return_inline
    #
    # # ==================== Обработчик инлайн кнопок==================================================
    #
    # def list_goal_keyboard(self, list_itm):
    #     """
    #     Создает разметку для основного меню
    #     """
    #     self.markup = InlineKeyboardMarkup(self.set_btn_inline(list_itm))
    #     return self.markup

    # =============== Стартовое меню после верификации=======================================================

    def start_menu(self):
        """
        Создает разметку кнопок для пользователя который в первый раз
        """
        list_itm = ['FINANCE', 'INFO', 'SETTINGS']
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup

    # =============== Меню финансы для пользователя 1 =======================================================

    def menu_fin_1(self):
        """
        Создает разметку кнопок для пользователя который в первый раз
        """
        list_itm = ['Add_goal']
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup

    def menu_fin_2(self):
        """
        Создает разметку кнопок для пользователя который в первый раз
        """
        list_itm = ['Add_income']
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup

    def menu_fin_3(self):
        """
        Создает разметку кнопок для пользователя который в первый раз
        """
        list_itm = ['List_goal', 'Edit_goal', 'Add_goal', 'List_income', 'Edit_income', 'Add_income', ]
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup

    # ======================================================================
    def goal_menu_1(self):
        """
        Создает разметку кнопок для работы с финансами
        """
        list_itm = ['GOAL_1']
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup

    # ------------------- menu 2 --------------------------------------

    def start_menu_2(self):
        """
        Создает разметку кнопок для пользователя который был, но нет целей
        """
        list_itm = ['ADD_GOAL', 'INFO', 'SETTINGS']
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup

    def start_menu_3(self):
        """
        Создает разметку кнопок для пользователя который был и есть цели
        """
        list_itm = ['GOAL_EDIT', 'INFO', 'SETTINGS']
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup

    def info_menu(self):
        """
        Создает разметку кнопок в меню 'О магазине'
        """
        list_itm = ['<<']
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup

    def settings_menu(self):
        """
        Создает разметку кнопок в меню 'Настройки'
        """
        list_itm = ['<<']
        self.markup = ReplyKeyboardMarkup(keyboard=self.set_btn(list_itm), one_time_keyboard=True)
        return self.markup
