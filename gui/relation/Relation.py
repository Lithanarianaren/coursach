from tkinter import W, END
from tkinter.ttk import Treeview
from typing import Optional

from gui.relation.Relationable import Relationable


class Relation(Treeview):

    def __init__(self, master, object_type: type, **kw):

        if not issubclass(object_type, Relationable):
            raise TypeError("Tried to pass a non-Relationable class to a Relation")

        super().__init__(master, show='headings', columns=object_type.get_relation_attributes(), **kw)

        self.__object_type: type = object_type
        self.__headers: tuple[str] = object_type.get_relation_attributes()
        self.__data: list = [Relationable]

        for header in self.__headers:
            self.heading(header, text=header)
            self.column(header, anchor=W)

    def set_data(self, data: list):
        for entry in data:
            if not isinstance(entry,self.__object_type):
                raise TypeError(f"Tried to pass a(n) {type(entry)} to a Relation of {self.__object_type}s")
        self.__data = data

    def show_data(self):
        for item in self.__data:
            if not issubclass(self.__object_type, Relationable):
                raise TypeError("Relation.__object_type is supposed to be private!")
            if not isinstance(item, self.__object_type):
                continue
            item_projection = item.get_relation_object()
            self.insert('', END, values=item_projection)

    def get_selected_index(self) -> Optional[int]:
        sel=self.selection()
        if not sel: return None
        return self.index(sel[0])

    def get_selected_item(self) -> Optional[Relationable]:
        ind = self.get_selected_index()
        if ind is None: return None
        return self.__data[ind]
