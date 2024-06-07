from tkinter import W, END, VERTICAL, ttk, Canvas, NW
from tkinter.ttk import Treeview, Frame
from typing import Optional

from gui.event.Event import Event
from gui.event.Listener import Listener
from gui.relation.Relationable import Relationable, HasInternalRelations
from gui.widgets.RelationElement import RelationElement




class Relation(Listener, Frame):

    def set_yview(self,y):
        self.update_idletasks()
        self.canvas.yview_moveto(y)


    def get_yview(self):
        return self.canvas.yview()[0]

    def __init__(self, master: ttk.Frame, object_type: type[Relationable], **kw):
        self.__parent_obj=None
        if not issubclass(object_type, Relationable):
            raise TypeError("Tried to pass a non-Relationable class to a Relation")
        super().__init__(master, **kw)

        self.__object_type: type[Relationable] = object_type
        self.__headers: list[str] = object_type.get_relation_attributes()
        self.__data: list = [Relationable]
        self.configure(borderwidth=0, padding=0)
        self.upper_frame = RelationElement(master=self)
        self.upper_frame.add_listener(self)
        self.upper_frame.place(x=0, y=0, relwidth=1, height=40)
        self.lower_frame = Frame(self)
        self.lower_frame.place(x=0, y=40, relwidth=1, height=-40, relheight=1)
        self.canvas = Canvas(self.lower_frame, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas)
        self.frame.place(x=0, y=0, relheight=1, relwidth=1)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self._frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw",
                                                   tags="self.frame")
        self.canvas.bind("<Configure>", self.resize_frame)

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

    def resize_frame(self, e):
        self.canvas.itemconfig(self._frame_id, width=e.width)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        speed = 1 / 6
        units = event.delta / 120
        fraction = self.vsb.get()[0] - units * speed

        fraction = max(0, fraction)
        self.canvas.yview_moveto(fraction)


    def set_data(self, data: list[Relationable], parent_obj:HasInternalRelations):
        for entry in data:
            if not isinstance(entry, self.__object_type):
                raise TypeError(f"Tried to pass a(n) {type(entry)} to a Relation of {self.__object_type}s")
        self.__data = data
        self.__parent_obj=parent_obj

    def show_data(self):
        self.upper_frame.fill_class(self.__object_type, self.__parent_obj)
        for i, item in enumerate(self.__data):
            if not issubclass(self.__object_type, Relationable):
                raise TypeError("Relation.__object_type is supposed to be private!")
            if not isinstance(item, self.__object_type):
                continue
            elem = RelationElement(master=self.frame)
            elem.fill_item(item, self.__parent_obj)
            elem.add_listener(self)
            elem.pack(fill='x', expand=True)
            # self.insert('', END, values=item)

    def receive_event(self, event: Event):
        self.send_event(event)
