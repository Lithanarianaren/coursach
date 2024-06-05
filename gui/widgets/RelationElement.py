from tkinter import ttk
from tkinter.ttk import Frame

from classes import Transaction, Worker
from gui.event.Event import Event
from gui.event.Listener import Listener
from gui.relation.Relationable import HasInternalRelations, Deletable
from gui.relation.Relationable import Relationable, Addable, Editable


class RelationElement(Listener, Frame):
    button_len = 110

    def receive_event(self, event: Event):
        pass

    def __init__(self, **kw):
        super().__init__(**kw, height=40, padding='5', relief='solid', style='Element.TFrame')
        self.item = None
        self.offset = 0
        self.length = 0
        self.labels: list[ttk.Label] = []
        self.add_button = None
        self.edit_button = None
        self.delete_button = None
        self.rel_button = None

    @staticmethod
    def calc_offset(type_rel: type[Relationable]):
        class_offset = RelationElement.button_len * issubclass(type_rel, Addable)
        item_offset = RelationElement.button_len * (
                issubclass(type_rel, HasInternalRelations) +
                issubclass(type_rel, Editable) +
                issubclass(type_rel, Deletable) +
                issubclass(type_rel, Transaction)
        )
        return max(class_offset, item_offset)

    def wrap_labels(self):
        for i in self.labels:
            i.config(wraplength=((self.winfo_width() - self.offset) / self.length - 10))

    def fill_item(self, item: Relationable):
        self.item = item
        self.offset = self.calc_offset(self.item.__class__)
        obj = item.get_relation_object()
        self.length = len(obj)
        length = self.length

        for i, t in enumerate(obj):
            label = ttk.Label(self, text=t, background='white')
            label.place(rely=0.5, relx=i / length, x=-self.offset / length * i, anchor='w', bordermode='inside')

            self.labels.append(label)
        offset = self.offset
        if isinstance(item, Transaction):
            if not item.completed:
                rel_button = ttk.Button(self, text="Провести")
                rel_button.place(rely=0.5, relx=1, x=-offset, anchor='w', bordermode='inside')
                offset -= RelationElement.button_len
                rel_button.bind("<Button-1>", self.clicked_trn)
        if isinstance(item, Worker):
            rel_button = ttk.Button(self, text="Зарплата")
            rel_button.place(rely=0.5, relx=1, x=-offset, anchor='w', bordermode='inside')
            offset -= RelationElement.button_len
            rel_button.bind("<Button-1>", lambda e: self.send_event(Event('pay_me',{'item':self.item})))
        if isinstance(item, HasInternalRelations):
            self.rel_button = ttk.Button(self, text="Таблицы...")
            self.rel_button.place(rely=0.5, relx=1, x=-offset, anchor='w', bordermode='inside')
            offset -= RelationElement.button_len
            self.rel_button.bind("<Button-1>", self.clicked_rel)
        if isinstance(item, Editable):
            if item.can_be_edited():
                rel_button = ttk.Button(self, text="Изменить...")
                rel_button.place(rely=0.5, relx=1, x=-offset, anchor='w', bordermode='inside')
                offset -= RelationElement.button_len
                rel_button.bind("<Button-1>", self.clicked_edit)
        if isinstance(item, Deletable):
            if item.can_be_deleted():
                rel_button = ttk.Button(self, text="Удалить")
                rel_button.place(rely=0.5, relx=1, x=-offset, anchor='w', bordermode='inside')
                offset -= RelationElement.button_len
                rel_button.bind("<Button-1>", self.clicked_delete)
        self.bind('<Configure>', lambda e: self.wrap_labels())

    def fill_class(self, item: type[Relationable]):
        self.item = item
        obj = self.item.get_relation_attributes()
        self.offset = self.calc_offset(item)
        self.length = len(obj)
        length = self.length
        for i, t in enumerate(obj):
            label = ttk.Label(self, text=t, background='white')
            label.place(rely=0.5, relx=i / length, x=-self.offset / length * i, anchor='w', bordermode='inside')
            self.labels.append(label)
        offset = self.offset
        if issubclass(item, Worker):
            rel_button = ttk.Button(self, text="Выдать всем")
            rel_button.place(rely=0.5, relx=1, x=-offset, anchor='w', bordermode='inside')
            offset -= RelationElement.button_len
            rel_button.bind("<Button-1>", lambda e: self.send_event(Event('pay_all', {})))
        if issubclass(item, Addable):
            self.rel_button = ttk.Button(self, text="Добавить...")
            self.rel_button.place(rely=0.5, relx=1, x=-offset, anchor='w', bordermode='inside')
            offset -= RelationElement.button_len
            self.rel_button.bind("<Button-1>", self.clicked_add)
        self.bind('<Configure>', lambda e: self.wrap_labels())

    def clicked_rel(self, event):
        self.send_event(Event('internal_relation_query', {'item': self.item}))

    def clicked_add(self, event):
        self.send_event(Event('add_query', {'class': self.item}))

    def clicked_edit(self, event):
        self.send_event(Event('edit_query', {'item': self.item}))

    def clicked_delete(self, event):
        self.send_event(Event('delete_query', {'item': self.item}))

    def clicked_trn(self, event):
        self.send_event(Event('trn_query', {'item': self.item}))
