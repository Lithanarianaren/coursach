from tkinter import Menu, Toplevel

from bd.jsonSaveLoad import SavingJSON, LoadJSON
from classes import BaseTransaction, Worker, Store, System
from gui.event.Event import Event
from gui.event.Listener import Listener
from gui.form.Form import Form
from gui.layout.WindowLayout import WindowLayout
from gui.relation.Relationable import Addable, Editable
from gui.relation.Relationable import HasInternalRelations, Deletable
from gui.widgets.ItemFrame import ItemFrame


class Window(Listener, WindowLayout):

    def reset(self):
        for i in self._item_frames:
            i.destroy()

    def reassign(self, item: HasInternalRelations):
        self._item_frames: list[ItemFrame] = []
        self.__obj = item
        self.setup_tabs()

    def back(self):
        if len(self.__backstack):
            self.reset()
            self.reassign(self.__backstack.pop())
            self._tab_control.select(self.__tab_backstack.pop())

    def forward(self, item: HasInternalRelations):
        self.__backstack.append(self.__obj)
        self.__tab_backstack.append(self.get_tab_index())
        self.reset()
        self.reassign(item)

    def receive_event(self, event: Event):
        if event.name == 'trn_query':
            item = event.data["item"]
            if isinstance(item, BaseTransaction):
                item.complete()
                self.update_tabs()
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
                    datatype.add(event.data['parent'], form_result)
                    self.update_tabs()
            return
        if event.name == 'edit_query':
            if isinstance(event.data['item'], Editable):
                item: Editable = event.data['item']
                form_result = Form(item.edit_form_blueprint()).launch()
                if form_result is not None:
                    item.edit(form_result, event.data['parent'])
                self.update_tabs()
            return
        if event.name == 'delete_query':
            if isinstance(event.data['item'], Deletable):
                item: Deletable = event.data['item']
                item.delete(event.data['parent'])
                self.update_tabs()
            return
        if event.name == 'pay_me':
            if isinstance(event.data['item'], Worker) and isinstance(self.__obj, Store):
                item: Worker = event.data['item']
                item.get_salary(event.data['parent'])
                self.update_tabs()
            return
        if event.name == 'pay_all':
            if isinstance(event.data['parent'], Store):
                event.data['parent'].pay_all_workers()
                self.update_tabs()
            return

    TABLE_WIDTH = 750

    def __init__(self, obj: HasInternalRelations):
        super().__init__()

        self._item_frames: list[ItemFrame] = []
        self.__obj = obj
        self.__backstack: list[HasInternalRelations] = []
        self.__tab_backstack: list[int] = []
        self.setup_tabs()
        self.setup_menu()
        self.bind('<F5>',lambda e: SavingJSON.save_system(System.single_instance))
        self.bind('<F2>',lambda e: self.load_file())
        self.backbutton.bind("<Button-1>", lambda e: self.back())
        self.bind("<Escape>", lambda e: self.back())

    def setup_tabs(self):
        for name in self.__obj.get_relation_names():
            frame = ItemFrame(self._tab_control)
            frame.add_listener(self)
            self._item_frames.append(frame)
            self._item_frames[-1].grid(row=0, column=0, sticky='nsew')
            self._tab_control.add(self._item_frames[-1], text=name)
        self.fill_tabs()

    def fill_tabs(self):
        self.fill_desc(self.__obj)
        for i in range(len(self._item_frames)):
            self._item_frames[i].setup(self.__obj,
                                       self.__obj.get_relation_classes()[i], self.__obj.get_relation_data()[i])

    def update_tabs(self):
        self.fill_desc(self.__obj)
        for i in range(len(self._item_frames)):
            saved_position = self._item_frames[i].get_yview()
            self._item_frames[i].setup(self.__obj,
                                       self.__obj.get_relation_classes()[i], self.__obj.get_relation_data()[i])
            self._item_frames[i].set_yview(saved_position)

    def setup_menu(self):
        self.option_add('*tearOff', False)
        self.toplevel = self.winfo_toplevel()
        self.menu = Menu(self)
        self.toplevel['menu'] = self.menu
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(menu=self.file_menu, label="Файл")
        self.file_menu.add_command(label="Сохранить", accelerator="F5",
                                   command=lambda: SavingJSON.save_system(System.single_instance))
        self.file_menu.add_command(label="Загрузить", accelerator="F2",
                                   command=lambda: self.load_file())

    def load_file(self):
        LoadJSON.load_system()
        self.__backstack=[]
        self.__tab_backstack=[]
        self.reset()
        self.reassign(System.single_instance)
