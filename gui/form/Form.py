from tkinter import Tk, TOP, X
from typing import Callable, Optional, Any, Union

from gui.form.FormElement import FormElementLayout
from gui.utilities import check_date


class Form:

    @staticmethod
    def int_constraint(value: str) -> tuple[Any, Optional[str]]:
        if value.isdigit():
            return int(value), None
        else:
            return None, "Не является числом"

    @staticmethod
    def str_constraint(value: str) -> tuple[Any, Optional[str]]:
        return int(value), None

    @staticmethod
    def date_constraint(value: str) -> tuple[Any, Optional[str]]:
        error_message = (None, "Не соответствует формату даты ДД.ММ.ГГГГ")
        elements = value.split('.')
        int_elements = [0, 0, 0]
        if len(elements) != 3: return error_message
        for i in range(3):
            if not elements[i].isdigit():
                return error_message
            int_elements[i] = int(elements[i])
        if not check_date(int_elements[0], int_elements[1], int_elements[2]):
            return None, "Ошибка в дате"
        return int_elements, None

    @staticmethod
    def unsigned_int_constraint(value: str) -> tuple[Any, Optional[str]]:
        constraint, message = Form.int_constraint(value)
        if message is None and constraint < 0:
            return None, "Не может быть отрицательным числом"
        else:
            return constraint, message

    def __init__(self):
        self.elements: list[FormElementLayout] = []

    def add(self, element: FormElementLayout):
        self.elements.append(element)
        return self

    def launch(self):
        window = Tk()
        window.minsize(400,100)
        window.maxsize(600,1080)
        for i in self.elements:
            i.make_frame(master=window)
            i.frame.pack(side=TOP,padx=20,pady=5,fill=X)
            #i.frame.pack_propagate(False)
