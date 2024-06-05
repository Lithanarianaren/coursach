from typing import Any, Optional, Callable

from gui.utilities import check_date

"""
Ограничения. Нужны в строковых формах - по факту, функции, которые проверяют строку, введённую пользователем, на
соответствие таким-то условиям. Используются в создании чертежей форм; форматированные данные, которые они возвращают,
в таком же виде поступают к тебе в функции создания/изменения. Вторым значением возвращает сообщение об ошибке.
Если нужны ещё ограничения - спокойно их пиши, ничего не должно сломаться.
"""


def int_constraint(value: str) -> tuple[Any, Optional[str]]:
    if value.isdigit():
        return int(value), None
    else:
        return None, "Не является числом"


def str_constraint(value: str) -> tuple[Any, Optional[str]]:
    return value, None


def date_constraint(value: str) -> tuple[Any, Optional[str]]:
    error_message = (None, "Не соответствует формату даты ДД.ММ.ГГГГ")
    elements = value.split('.')
    int_elements = [0, 0, 0]
    if len(elements) != 3:
        return error_message
    for i in range(3):
        if not elements[i].isdigit():
            return error_message
        int_elements[i] = int(elements[i])
    if not check_date(int_elements[0], int_elements[1], int_elements[2]):
        return None, "Ошибка в дате"
    return int_elements, None


def unsigned_int_constraint(value: str) -> tuple[Any, Optional[str]]:
    constraint, message = int_constraint(value)
    if message is None and constraint < 0:
        return None, "Не может быть отрицательным числом"
    else:
        return constraint, message



class ElementBlueprint:
    """
    Класс чертежа элемента формы: один элемент - одна переменная в форме. Объединяет их в общем только одно: у них
    есть имя.
    """

    def __init__(self, name: str):
        self.name = name


class TextElem(ElementBlueprint):
    """
    Любой элемент, где пользователь вбивает текст. Форматирование определяется полем constraint.
    """

    def __init__(self, name: str, constraint: Callable[[str], tuple[Any, Optional[str]]], value=""):
        """
        :param name:
        :param constraint: имя одной из функций constraint. форма будет вызывать эту функцию для форматирования данных
        и защиты от пользователя.
        :param value: начальное значение. это для форм редактирования.
        """
        super().__init__(name)
        self.constraint = constraint
        self.value = value


class BoolElem(ElementBlueprint):
    """
    Элемент, где пользователь протыкивает галочку.
    """

    def __init__(self, name, value=False):
        super().__init__(name)

        self.value = value


class ListElem(ElementBlueprint):
    """
    Элемент, где пользователь выбирает из списка.
    """

    def __init__(self, name, values: list[str], value=0, lock=True):
        """
        :param name:
        :param values: список строк, из которого пользователь будет выбирать
        :param value: численный индекс строки, на которую упадёт выбор по умолчанию
        :param lock: если равен True, пользователю нельзя вводить свои данные
        """
        super().__init__(name)
        self.values = values
        self.value = value
        self.lock = lock


class FormBlueprint:
    """
    Чертёж формы. Содержит в себе несколько чертежей элементов формы. Подаётся на выход запроса чертежа формы.
    """

    def __init__(self):
        """
        да, весь класс - по факту список)
        """
        self.elements: list[ElementBlueprint] = []

    def add(self, element: ElementBlueprint):
        """
        вот эта функция поддерживает следующие конструкции:
        FormBlueprint() \
            .add(...) \
            .add(...) \
            .add(...)
        ну и так далее. очень удобная штука)

        реально удобно
        """
        self.elements.append(element)
        return self
