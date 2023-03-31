from db.models import User_verification, Purposes, Income, Expenses_needs  # TODO: Импорт должен быть по другому

class DBManager:
    """
    Класс менеджер для работы с БД
    """

    def __init__(self):
        pass

    def select_db_user_verification(self):
        """Получаем результат из БД таблицы User_verification"""
        result = User_verification.objects.all().values_list('user_id', 'user_name', 'activating_bot_goal', 'activating_bot_income')
        return result

    def select_db_purposes(self):
        """Получаем результат из БД таблицы Purposes"""
        result = Purposes.objects.all().values_list('user_id_purposes', 'codename', 'category', 'aliases', 'price',
                                                    'data')
        return result

    def select_db_income(self):
        """Получаем результат из БД, таблица Income"""
        result = Income.objects.all().values_list('user_id_purposes',
                                                  'price',
                                                  'title_income'
                                                  )
        return result

    def insert_db_purposes(self, user_id_purposes, codename, category, aliases, price, data):
        """Добавление цели в БД таблица Purposes"""
        result = Purposes.objects.create(user_id_purposes=user_id_purposes,
                                         codename=codename,
                                         category=category,
                                         aliases=aliases,
                                         price=price,
                                         data=data
                                         )
        return

    def insert_db_income(self, user_id_purposes, price, title_income):
        """Добавление дохода в БД таблица Income"""
        result = Income.objects.create(user_id_purposes=user_id_purposes,
                                       price=price,
                                       title_income=title_income
                                       )
        return

    def insert_db_user_verification(self, user_id, user_name, activating_bot_goal, activating_bot_income):
        """Добавление пользователя в БД таблица User_verification"""
        result = User_verification.objects.create(user_id=user_id,
                                                  user_name=user_name,
                                                  activating_bot_goal=activating_bot_goal,
                                                  activating_bot_income=activating_bot_income
                                                  )
        return

    def insert_db_expenses_needs(self, user_id_purposes, codename, category, aliases, price, quantity, raw_text):
        """Добавление расхода в БД таблица Expenses_needs"""
        result = Expenses_needs.objects.create(user_id_purposes = user_id_purposes,
                                               codename = codename,
                                               category = category,
                                               aliases = aliases,
                                               price = price,
                                               quantity = quantity,
                                               raw_text = raw_text)
        return

    def delete_db_purposes(self, user_id_purposes, codename, category, aliases, price, data):
        """Удаление цели из БД, таблица Purposes"""
        delete_db = Purposes.objects.get(user_id_purposes=user_id_purposes,
                                         codename=codename,
                                         category=category,
                                         aliases=aliases,
                                         price=price,
                                         data=data)
        delete_db.delete()
        return

    def delete_db_income(self, user_id_purposes, price, title_income):
        """Удаление дохода из БД, таблица Income"""
        delete_db = Income.objects.get(user_id_purposes=user_id_purposes,
                                       price=price,
                                       title_income=title_income
                                       )
        delete_db.delete()
        return

    def delete_db_user_verification(self, user_id, user_name, activating_bot_goal, activating_bot_income):
        """Удаление пользователя из БД, таблица User_verification"""
        delete_db = User_verification.objects.get(user_id=user_id,
                                                  user_name=user_name,
                                                  activating_bot_goal=activating_bot_goal,
                                                  activating_bot_income=activating_bot_income
                                                  )
        delete_db.delete()
        return
