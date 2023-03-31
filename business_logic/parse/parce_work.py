class List_parce_message:
    """Структура распаршенного сообщения о новом расходе"""

    def __init__(self, price, quantity, alias, raw_text):
        self.price = price
        self.quantity = quantity
        self.alias = alias
        self.raw_text = raw_text


class Parse_message:
    """Класс для парсинга сообщенеия"""

    def __init__(self):
        self.list_parse = []

    def list_from_message(self, text_message):
        """Парсит сообщение и загружает в list_parse"""
        text_parce = text_message.message.text
        price = int(text_parce.split(' ')[0])
        quantity = int(text_parce.split(' ')[1])
        aliases = text_parce.split(' ')[2]

        object_parse = List_parce_message(
            price=price,
            quantity=quantity,
            alias=aliases,
            raw_text=text_parce
        )
        self.list_parse.append(object_parse)
        return self.list_parse


