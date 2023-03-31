from db.db_work import DBManager


class Income_list:
    """Структура доходов пользователя из БД"""

    def __init__(self, number_goal, user_id_purposes, price, title_income):
        self.number_goal = number_goal
        self.user_id_purposes = user_id_purposes
        self.price = price
        self.title_income = title_income


class Income:
    """Класс для работы с доходами """

    def __init__(self, ):
        self.BD = DBManager()
        self.list_income = []

    def load_income(self):  # TODO: Вынести в отдельный файл
        """Возвращает список доходов из БД"""
        number_goal = 0
        # Получаем результат из БД таблицы User_verification
        self.list_income.clear()
        list_goal = self.BD.select_db_income()
        # Проходимся по списку
        for income in list_goal:
            number_goal += 1
            user_id_purposes = income[0],
            price = income[1]
            title_income = income[2]
            # Заносим в шаблон
            user_object = Income_list(
                user_id_purposes=user_id_purposes[0],
                number_goal=number_goal,
                price=price,
                title_income=title_income
            )
            self.list_income.append(user_object)
        return self.list_income
