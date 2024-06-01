from tkinter import ttk, LEFT, X, StringVar, RIGHT, BooleanVar
from typing import Callable, Any, Optional


class FormElementLayout:
    def __init__(self, name: str):
        self.name = name
        self.frame = None
        self.input = None
        self.var = None
        self.label = None

    def get(self):
        raise NotImplementedError

    def generate_frame(self, **kw):
        self.frame = ttk.Frame(**kw)
        self.label = ttk.Label(self.frame, text=self.name)
        self.frame.bind('<Configure>', lambda e: self.label.config(wraplength=self.frame.winfo_width() // 2))
        self.label.pack(side=LEFT, fill=X)

    def make_frame(self, **kw):
        raise NotImplementedError


class TextFormElement(FormElementLayout):

    def __init__(self, name, constraint: Callable[[str], tuple[Any, Optional[str]]], value=""):
        super().__init__(name)
        self.var = StringVar()
        self.var.set(value)
        self.constraint = constraint

    def get(self):
        return self.constraint(self.input.get())

    def make_frame(self, **kw):
        self.generate_frame(**kw)
        self.input = ttk.Entry(self.frame)
        self.input.insert(0,self.var.get())
        self.input.pack(side=RIGHT)


class BoolFormElement(FormElementLayout):

    def __init__(self, name, value=False):
        super().__init__(name)

        self.value = value

    def get(self):
        return self.var.get(), None

    def make_frame(self, **kw):
        self.generate_frame(**kw)
        self.input = ttk.Checkbutton(self.frame)
        self.var = BooleanVar(self.input)
        self.input.config(variable=self.var)
        self.var.set(self.value)
        self.input.state(['!alternate'])
        self.input.state([''])
        self.input.pack(side=RIGHT)


class SelectionFormElement(FormElementLayout):

    def __init__(self, name, values: list[str], value=0, lock=True):
        super().__init__(name)
        self.var = StringVar()
        self.values = values
        self.value = value
        self.lock=lock

    def get(self):
        return self.input.get(), None

    def make_frame(self, **kw):
        self.generate_frame(**kw)
        self.input = ttk.Combobox(self.frame, values=self.values)
        if self.lock:
            self.input.config(state='readonly')
        self.input.current(self.value)
        self.input.pack(side=RIGHT)
