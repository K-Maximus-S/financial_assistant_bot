from db.db_work import DBManager


class Goal_list:
    """Структура целей пользователя из БД"""

    def __init__(self, number_goal, user_id_purposes, codename, category, aliases, price, data):
        self.number_goal = number_goal
        self.user_id_purposes = user_id_purposes
        self.codename = codename
        self.category = category
        self.aliases = aliases
        self.price = price
        self.data = data

class Goal:
    """Класс работы с целями"""

    def __init__(self, ):
        self.BD = DBManager()
        self.list_goall = []


    def load_purposes(self):
        """Возвращает список целей из БД"""
        number_goal = 0
        # Получаем результат из БД таблицы User_verification
        self.list_goall.clear()
        list_goal = self.BD.select_db_purposes()
        # Проходимся по списку
        for goal in list_goal:
            number_goal += 1
            user_id_purposes = goal[0],
            codename = goal[1],
            category = goal[2],
            aliases = goal[3],
            price = goal[4],
            data = goal[5],
            # Заносим в шаблон
            user_object = Goal_list(
                user_id_purposes=user_id_purposes[0],
                codename=codename[0],
                category=category[0],
                aliases=aliases[0],
                price=price[0],
                data=data[0],
                number_goal=number_goal
            )
            self.list_goall.append(user_object)
        return self.list_goall
