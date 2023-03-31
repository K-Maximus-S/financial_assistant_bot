from business_logic.goal.goal_work import Goal
from business_logic.income.income_work import Income
from db.db_work import DBManager


class Verification_result:
    """Структура user из БД"""

    def __init__(self, user_id, user_name, activating_bot_goal, activating_bot_income):
        self.user_id = user_id
        self.user_name = user_name
        self.activating_bot_goal = activating_bot_goal
        self.activating_bot_income = activating_bot_income


class Verification:
    """Класс идентификации"""

    def __init__(self):
        self.BD = DBManager()
        self.goal = Goal()
        self.income = Income()
        self.list_user = []
        self.list_user_menu = []

    def load_user_verification(self):
        """Возвращает список пользователей из БД"""
        # Получаем результат из БД таблицы User_verification
        self.list_user.clear()
        user_verification = self.BD.select_db_user_verification()
        # Проходимся по списку
        for verification_list in user_verification:
            user_id = (verification_list[0])
            user_name = (verification_list[1])
            activating_bot_goal = (verification_list[2])
            activating_bot_income = (verification_list[3])
            # Заносим в шаблон
            user_object = Verification_result(
                user_id=user_id,
                user_name=user_name,
                activating_bot_goal=activating_bot_goal,
                activating_bot_income=activating_bot_income
            )
            self.list_user.append(user_object)

    def user_verification(self, update):
        """
            Проверяем пользователя:
                1) Пользователь -, цели -, доход -
                2) Пользователь +, цели +, доход -
                3) Пользователь +, цели -, доход +
                4) Пользователь +, цели +, доход +
                5) Пользователь +, цели -, доход -
        """
        self.load_user_verification()
        log_menu = None
        text_result = None
        user_id = None

        user_id = None
        user_name = None
        activating_bot_goal = None
        activating_bot_income = None

        for verification in self.list_user:
            user_id = int(verification.user_id)
            user_name = verification.user_name
            activating_bot_goal = verification.activating_bot_goal
            activating_bot_income = verification.activating_bot_income

            if update.message.from_user.id == user_id and update.message.from_user.name == user_name:
                log_menu = 'True'
                user_id = user_id
                user_name = user_name
                activating_bot_goal = activating_bot_goal
                activating_bot_income = activating_bot_income
                break
            elif update.message.from_user.id != user_id and update.message.from_user.name != user_name:
                log_menu = 'False'

        if log_menu == 'False':
            # Для 1
            if update.message.from_user.id != user_id and update.message.from_user.name != user_name:
                text_result = 1

        elif log_menu == 'True':
            # Для 2
            if update.message.from_user.id == user_id and update.message.from_user.name == user_name and activating_bot_goal == 'True' and activating_bot_income == 'False':
                text_result = 2
            # Для 3
            elif update.message.from_user.id == user_id and update.message.from_user.name == user_name and activating_bot_goal == 'False' and activating_bot_income == 'True':
                text_result = 3
            # Для 4
            elif update.message.from_user.id == user_id and update.message.from_user.name == user_name and activating_bot_goal == 'True' and activating_bot_income == 'True':
                text_result = 4
            # Для 5
            elif update.message.from_user.id == user_id and update.message.from_user.name == user_name and activating_bot_goal == 'False' and activating_bot_income == 'False':
                text_result = 5

        return text_result

    def edit_verification(self, update, verification_result):
        """
            Проверяем пользователя:
                1) Пользователь - ,  goal -, income - -> Добавить нового пользователя с новой целью
                2) Пользователь + ,  goal +, income  - -> Удаляю False из activating_bot_income, добавляю новый доход(первый)
                3) Пользователь + ,  goal -, income + -> Удаляю False из activating_bot_goal, добавляю новую цель(первую)
                4) Пользователь + ,  activating_bot_goal +, goal_logis  + -> (Пользователь может добавить цель или доход)
                                                                                (Иди удалить цели или доходы
                5) Пользователь + ,  goal -, income  - -> (Пользователь может добавить цель или доход)

        """
        log_goal = None
        log_income = None
        if verification_result == 1:
            self.BD.insert_db_user_verification(user_id=update.message.from_user.id,
                                                user_name=update.message.from_user.name,
                                                activating_bot_goal='True',
                                                activating_bot_income='False'
                                                )

        elif verification_result == 2:
            list_income = self.income.load_income()
            self.load_user_verification()

            # Проверка: есть ли в БД User_verification
            for verification in self.list_user:
                user_id = int(verification.user_id)
                user_name = verification.user_name
                activating_bot_goal = verification.activating_bot_goal
                activating_bot_income = verification.activating_bot_income
                if update.message.from_user.id == user_id and activating_bot_goal == 'True' and activating_bot_income == 'False':

                    # Проверка: Если ли в БД цели
                    for income_id in list_income:
                        user_id_purposes_goal = int(income_id.user_id_purposes)
                        if update.message.from_user.id == user_id_purposes_goal:
                            log_income = 'True'
                            break
                        elif update.message.from_user.id != user_id_purposes_goal:
                            log_income = 'False'
                    # Добавляем первый доход
                    if log_income == 'True':
                        self.BD.delete_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='True',
                                                            activating_bot_income='False'
                                                            )
                        self.BD.insert_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='True',
                                                            activating_bot_income='True'
                                                            )
                        break

        elif verification_result == 3:
            list_income = self.income.load_income()
            list_goal = self.goal.load_purposes()
            self.load_user_verification()

            # Проверка: есть ли в БД User_verification
            for verification in self.list_user:
                user_id = int(verification.user_id)
                user_name = verification.user_name
                activating_bot_goal = verification.activating_bot_goal
                activating_bot_income = verification.activating_bot_income
                if update.message.from_user.id == user_id and activating_bot_goal == 'False' and activating_bot_income == 'True':

                    # Проверка: Если ли в БД цели
                    for goal_id in list_goal:  # 44444
                        user_id_purposes_goal = int(goal_id.user_id_purposes)
                        if update.message.from_user.id == user_id_purposes_goal:
                            log_goal = 'True'
                            break
                        elif update.message.from_user.id != user_id_purposes_goal:
                            log_goal = 'False'
                    # Добавляем первую цель
                    if log_goal == 'True':
                        self.BD.delete_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='False',
                                                            activating_bot_income='True'
                                                            )
                        self.BD.insert_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='True',
                                                            activating_bot_income='True'
                                                            )
                        break

        elif verification_result == 4:
            list_income = self.income.load_income()
            list_goal = self.goal.load_purposes()
            self.load_user_verification()

            # Проверка: есть ли в БД User_verification
            for verification in self.list_user:
                user_id = int(verification.user_id)
                user_name = verification.user_name
                activating_bot_goal = verification.activating_bot_goal
                activating_bot_income = verification.activating_bot_income
                if update.message.from_user.id == user_id and activating_bot_goal == 'True' and activating_bot_income == 'True':

                    # Проверка: Если ли в БД цели
                    for goal_id in list_goal:
                        user_id_purposes_goal = int(goal_id.user_id_purposes)
                        if update.message.from_user.id == user_id_purposes_goal:
                            log_goal = 'True'
                            break
                        elif update.message.from_user.id != user_id_purposes_goal:
                            log_goal = 'False'
                    # Удаление последней цели
                    if log_goal == 'False':
                        self.BD.delete_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='True',
                                                            activating_bot_income='True'
                                                            )
                        self.BD.insert_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='False',
                                                            activating_bot_income='True'
                                                            )
                        break

                    # Проверка: Если ли в БД доходы
                    for income_id in list_income:
                        user_id_purposes_income = int(income_id.user_id_purposes)
                        if update.message.from_user.id == user_id_purposes_income:
                            log_income = 'True'
                            break
                        elif update.message.from_user.id != user_id_purposes_income:
                            log_income = 'False'
                    # Удаление последнего дохода
                    if log_income == 'False':
                        self.BD.delete_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='True',
                                                            activating_bot_income='True'
                                                            )
                        self.BD.insert_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='True',
                                                            activating_bot_income='False'
                                                            )
                        break
        elif verification_result == 5:
            list_income = self.income.load_income()
            list_goal = self.goal.load_purposes()
            self.load_user_verification()

            # Проверка: есть ли в БД User_verification
            for verification in self.list_user:
                user_id = int(verification.user_id)
                user_name = verification.user_name
                activating_bot_goal = verification.activating_bot_goal
                activating_bot_income = verification.activating_bot_income
                if update.message.from_user.id == user_id and activating_bot_goal == 'False' and activating_bot_income == 'False':

                    # Проверка: Если ли в БД цели
                    for goal_id in list_goal:
                        user_id_purposes_goal = int(goal_id.user_id_purposes)
                        if update.message.from_user.id == user_id_purposes_goal:
                            log_goal = 'True'
                        elif update.message.from_user.id != user_id_purposes_goal:
                            log_goal = 'False'
                    # Пользователь все первую цель
                    if log_goal == 'True':
                        self.BD.delete_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='False',
                                                            activating_bot_income='False'
                                                            )
                        self.BD.insert_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='True',
                                                            activating_bot_income='False'
                                                            )
                        break

                    # Проверка: Если ли в БД доходы
                    for income_id in list_income:
                        user_id_purposes_income = int(income_id.user_id_purposes)
                        if update.message.from_user.id == user_id_purposes_income:
                            log_income = 'True'
                        elif update.message.from_user.id != user_id_purposes_income:
                            log_income = 'False'
                    # Пользователь добавил первый доход
                    if log_income == 'True':
                        self.BD.delete_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='False',
                                                            activating_bot_income='False'
                                                            )
                        self.BD.insert_db_user_verification(user_id=update.message.from_user.id,
                                                            user_name=update.message.from_user.name,
                                                            activating_bot_goal='False',
                                                            activating_bot_income='True'
                                                            )
                        break
