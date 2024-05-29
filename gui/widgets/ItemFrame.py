from tkinter import ttk

from gui.event.Event import Event
from gui.event.Listener import Listener
from gui.relation.HasInternalRelations import HasInternalRelations
from gui.widgets.Relation import Relation


class ItemFrame(Listener, ttk.Frame):
    def __init__(self, master):
        super(ItemFrame, self).__init__(master)
        self.relation = None
        self.lookup_button = None

    def setup(self, obj_type, width, data):
        self.relation = Relation(self, obj_type)
        self.relation.add_listener(self)
        self.relation.set_data(data)
        self.relation.show_data()
        self.relation.place(x=0,y=0,relheight=1,relwidth=1)
        #if issubclass(obj_type, HasInternalRelations):
        #    self.lookup_button = ttk.Button(self, command=lambda: self.lookup())
        #    self.lookup_button.grid(row=1, column=0)


    def receive_event(self, event: Event):
        self.send_event(event)

    def __del__(self):
        del self.relation
