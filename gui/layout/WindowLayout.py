from tkinter import Tk, ttk, Frame

from gui.event.Event import Event
from gui.event.Listener import Listener
from gui.relation.Relationable import Relationable, HasInternalRelations


class WindowLayout(Tk):

    def __init__(self):
        super().__init__()
        # self.eval('tk::PlaceWindow . center')
        self.minsize(1200, 800)
        self.geometry('1200x800')
        self.object_desc = ttk.Frame(self, padding="10", relief='groove')
        self.object_desc.place(anchor='nw', relwidth=1, relheight=0.2, x=10, y=10, width=-20, height=-20)
        self.backbutton = ttk.Button(self.object_desc, text='Назад')
        self.backbutton.place(anchor='nw', width=50, height=25)
        self.desc_frame = ttk.Frame(self.object_desc,relief='solid')
        self.desc_frame.place(anchor='nw',relwidth=1,relheight=1,height=-35, y=35)
        self.class_label = ttk.Label(self.object_desc,text="Система")
        self.class_label.place(anchor='nw',x=70,y=3)
        self._tab_control = ttk.Notebook(self)
        self._tab_control.place(anchor='nw', x=10, y=0, relwidth=1, relheight=0.8, rely=0.2, width=-20, height=-10)
        # self._tab_control.pack(expand=1, fill='both')

    def fill_desc(self, item:HasInternalRelations):
        self.class_label.config(text=item.get_class_name())
        headers = item.get_relation_attributes()
        values = item.get_relation_object()
        self.desc_frame.destroy()
        self.desc_frame = ttk.Frame(self.object_desc)
        self.desc_frame.place(anchor='nw', relwidth=1, relheight=1, height=-35, y=35)
        for header, value in zip(headers,values):
            ttk.Label(self.desc_frame, text=f"{header}: {value}").pack(side='top',fill='x')

    def get_tab_index(self):
        return self._tab_control.index(self._tab_control.select())
