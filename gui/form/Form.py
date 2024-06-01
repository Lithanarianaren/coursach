from tkinter import Tk, TOP, messagebox

from gui.form.FormElement import *
from gui.form.blueprints import *
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
        if len(elements) != 3:
            return error_message
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

    def __init__(self, blueprint: FormBlueprint = None):
        self.elements: list[FormElementLayout] = []
        self.answer = None
        if blueprint is not None:
            for element in blueprint.elements:
                self.add_from_blueprint(element)

    def add_from_blueprint(self, blueprint: ElementBlueprint):
        if isinstance(blueprint, TextElem):
            self.add(TextFormElement(blueprint.name, blueprint.constraint, blueprint.value))
        elif isinstance(blueprint, BoolElem):
            self.add(BoolFormElement(blueprint.name, blueprint.value))
        elif isinstance(blueprint, ListElem):
            self.add(SelectionFormElement(blueprint.name, blueprint.values, blueprint.value, blueprint.lock))

    def add(self, element: FormElementLayout):
        self.elements.append(element)
        return self

    @staticmethod
    def cancel(wnd):
        wnd.quit()
        wnd.destroy()

    def confirm(self, wnd):
        answer = []
        for element in self.elements:
            elem_ans = element.get()
            if elem_ans[1] is not None:
                messagebox.showerror("Ошибка ввода", element.name + ": " + elem_ans[1])
                wnd.lift()
                return
            answer.append(elem_ans[0])
        self.answer = answer
        wnd.quit()
        wnd.destroy()

    def launch(self):

        window = Tk()
        window.protocol("WM_DELETE_WINDOW", lambda: Form.cancel(window))
        window.minsize(400, 100)
        window.maxsize(600, 1080)
        for i in self.elements:
            i.make_frame(master=window)
            i.frame.pack(side=TOP, padx=20, pady=5, fill=X)
            # i.frame.pack_propagate(False)

        last_frame = ttk.Frame(window)
        last_frame.pack(side=TOP, padx=20, pady=5, fill=X)

        confirmButton = ttk.Button(last_frame, text='ОК', command=lambda: self.confirm(window))
        cancelButton = ttk.Button(last_frame, text='Отмена', command=lambda: Form.cancel(window))
        cancelButton.pack(side=RIGHT, padx=5)
        confirmButton.pack(side=RIGHT, padx=5, pady=5)
        window.resizable(False, False)
        window.mainloop()
        return self.answer
