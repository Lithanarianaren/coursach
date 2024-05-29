from tkinter import ttk, LEFT, X, StringVar, RIGHT, BooleanVar, IntVar
from typing import Callable, Any, Optional


class FormElementLayout:
    def __init__(self, name: str):
        self.name = name
        self.frame:ttk.Frame=None


    def get_value(self):
        raise NotImplementedError

    def generate_frame(self,**kw):
        self.frame = ttk.Frame(**kw)
        self.label = ttk.Label(self.frame, text=self.name)
        self.frame.bind('<Configure>', lambda e: self.label.config(wraplength=self.frame.winfo_width()//2))
        self.label.pack(side=LEFT, fill=X)

    def make_frame(self,**kw):
        raise NotImplementedError



class TextFormElement(FormElementLayout):
    def get_value(self):
        pass

    def __init__(self, name, constraint: Callable[[str], tuple[Any, Optional[str]]], value=""):
        super().__init__(name)
        self.string_var = StringVar()
        self.string_var.set(value)
        self.constraint = constraint


    def get(self):
        return self.constraint(self.string_var.get())

    def make_frame(self,**kw):
        self.generate_frame(**kw)
        self.input = ttk.Entry(self.frame, textvariable=self.string_var)
        self.input.pack(side=RIGHT)



class BoolFormElement(FormElementLayout):
    def get_value(self):
        pass

    def __init__(self, name, value=False):
        super().__init__(name)

        self.value=value


    def get(self):
        self.bool_var.get(), None

    def make_frame(self,**kw):
        self.generate_frame(**kw)
        self.input = ttk.Checkbutton(self.frame)
        self.bool_var = BooleanVar(self.input)
        self.input.config(variable=self.bool_var)
        self.bool_var.set(self.value)
        self.input.state(['!alternate'])
        self.input.state([''])
        self.input.pack(side=RIGHT)


class SelectionFormElement(FormElementLayout):
    def get_value(self):
        pass

    def __init__(self, name, values:list[str], value=0, **kw):
        super().__init__(name, **kw)
        self.string_var = StringVar()
        self.values=values
        self.value=value



    def get(self):
        return self.string_var.get(), None

    def make_frame(self,**kw):
        self.generate_frame(**kw)
        self.input = ttk.Combobox(self.frame, values=self.values, state='readonly')
        self.input.current(self.value)
        self.input.pack(side=RIGHT)
