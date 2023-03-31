from django.db import models

class User_verification(models.Model):
    """Таблица идентификации пользователя"""

    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=50, verbose_name='ID пользователя из телеграма')
    user_name = models.CharField(max_length=50, verbose_name='Имя пользователя из телеграма')
    activating_bot_goal = models.CharField(max_length=50, verbose_name='Активация бота по (Цель): True - есть цель, False - нет цели')
    activating_bot_income = models.CharField(max_length=50, verbose_name='Активация бота по (Доход): True - есть доход, False - нет дохода')

class Purposes(models.Model):
    """Таблица целей"""
    id = models.BigAutoField(primary_key=True)
    user_id_purposes = models.CharField(max_length=15, verbose_name='id пользователя телеграм')
    codename = models.CharField(max_length=50, verbose_name='Название раздела (Потребности|Инвестиции|Желания')
    category = models.CharField(max_length=50, verbose_name='Название категории (еда,жилье,тс, итд')
    aliases = models.CharField(max_length=50, verbose_name='Название алиаса (магазин:продукты:итд')
    price = models.IntegerField(verbose_name='Сумма')
    data = models.CharField(max_length=15, verbose_name='Дата')

class Income(models.Model):
    """Таблица доходов"""
    id = models.BigAutoField(primary_key=True)
    user_id_purposes = models.CharField(max_length=15, verbose_name='id пользователя телеграм')
    title_income = models.CharField(max_length=15, verbose_name='id пользователя телеграм')
    price = models.IntegerField(verbose_name='Сумма')

class Expenses_needs(models.Model):
    """Таблица расходов """
    id = models.BigAutoField(primary_key=True)
    user_id_purposes = models.CharField(max_length=15, verbose_name='id пользователя телеграм')
    codename = models.CharField(max_length=50, verbose_name='Название раздела (Потребности|Инвестиции|Желания')
    category = models.CharField(max_length=50, verbose_name='Название категории (еда,жилье,тс, итд')
    aliases = models.CharField(max_length=50, verbose_name='Название алиаса (магазин:продукты:итд')
    price = models.IntegerField(verbose_name='Сумма')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Количество')
    data_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    raw_text = models.TextField(verbose_name='Полный текст сообщения')