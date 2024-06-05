from tkinter.ttk import Frame

from classes import BaseTransaction, Worker, Store
from gui.event.Event import Event
from gui.event.Listener import Listener
from gui.form.Form import Form
from gui.layout.WindowLayout import WindowLayout
from gui.relation.Relationable import HasInternalRelations, Deletable
from gui.relation.Relationable import Addable, Editable
from gui.widgets.ItemFrame import ItemFrame


class Window(Listener, WindowLayout):

    def reset(self):
        for i in self._tabs:
            i.destroy()

    def reassign(self, item: HasInternalRelations):
        self._tabs: list[ItemFrame] = []
        self.__obj = item
        self.setup_tabs()
        self.fill_tabs()

    def back(self):
        if len(self.__backstack):
            self.reset()
            self.reassign(self.__backstack.pop())

    def forward(self, item: HasInternalRelations):
        self.__backstack.append(self.__obj)
        self.reset()
        self.reassign(item)

    def receive_event(self, event: Event):
        if event.name == 'trn_query':
            item = event.data["item"]
            if isinstance(item,BaseTransaction):
                item.complete()
                self.fill_tabs()
            return
        if event.name == 'internal_relation_query':
            if isinstance(event.data['item'], HasInternalRelations):
                self.forward(event.data['item'])
            return
        if event.name == 'add_query':
            if issubclass(event.data['class'], Addable):
                datatype: type[Addable] = event.data['class']
                form_result = Form(datatype.add_form_blueprint()).launch()
                if form_result is not None:
                    datatype.add(self.__obj, form_result)
                    self.fill_tabs()
            return
        if event.name == 'edit_query':
            if isinstance(event.data['item'], Editable):
                item: Editable = event.data['item']
                form_result = Form(item.edit_form_blueprint()).launch()
                if form_result is not None:
                    item.edit(form_result)
                self.fill_tabs()
            return
        if event.name == 'delete_query':
            if isinstance(event.data['item'], Deletable):
                item: Deletable = event.data['item']
                item.delete(self.__obj)
                self.fill_tabs()
            return
        if event.name == 'pay_me':
            if isinstance(event.data['item'], Worker) and isinstance(self.__obj, Store):
                item: Worker = event.data['item']
                item.get_salary(self.__obj)
                self.fill_tabs()
        if event.name == 'pay_all':
            if isinstance(self.__obj, Store):
                self.__obj.pay_all_workers()
                self.fill_tabs()

    TABLE_WIDTH = 750

    def __init__(self, obj: HasInternalRelations):
        super().__init__()

        self._tabs: list[ItemFrame] = []
        self.__obj = obj
        self.__backstack = []
        self.setup_tabs()
        self.fill_tabs()

        self.backbutton.bind("<Button-1>", lambda e: self.back())
        self.bind("<Escape>", lambda e: self.back())

    def setup_tabs(self):
        for name in self.__obj.get_relation_names():
            frame = ItemFrame(self._tab_control)
            frame.add_listener(self)
            self._tabs.append(frame)
            self._tabs[-1].grid(row=0, column=0, sticky='nsew')
            self._tab_control.add(self._tabs[-1], text=name)

    def fill_tabs(self):
        self.fill_desc(self.__obj)
        for i in range(len(self._tabs)):
            self._tabs[i].setup(self.__obj.get_relation_classes()[i], 750, self.__obj.get_relation_data()[i])
