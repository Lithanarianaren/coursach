from tkinter import ttk
from tkinter.ttk import Frame

from gui.event.Event import Event
from gui.event.Listener import Listener


class RelationElement(Listener, Frame):
    def receive_event(self, event: Event):
        pass

    def __init__(self, item, **kw):
        super().__init__(**kw, height=40, padding='5', relief='solid', style='Element.TFrame')
        self.item = item
        self.labels = []
        for i, t in enumerate(item.get_relation_object()):
            label = ttk.Label(self, text=t,background='white')
            label.grid(row=0, column=i)
            label.bind("<Button-1>", self.clicked)
            self.labels.append(label)
        self.bind("<Button-1>", self.clicked)

    def clicked(self, event):
        self.send_event(Event('item_clicked', {'item': self.item}))
