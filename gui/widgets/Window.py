from gui.event.Event import Event
from gui.event.Listener import Listener
from gui.layout.WindowLayout import WindowLayout
from gui.relation.HasInternalRelations import HasInternalRelations
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

    def back(self, none=None):
        if len(self.__backstack):
            self.reset()
            self.reassign(self.__backstack.pop())

    def forward(self, item: HasInternalRelations):
        self.__backstack.append(self.__obj)
        self.reset()
        self.reassign(item)

    def receive_event(self, event: Event):
        if event.name == 'item_clicked':
            if isinstance(event.data['item'], HasInternalRelations):
                self.forward(event.data['item'])

    TABLE_WIDTH = 750

    def __init__(self, obj: HasInternalRelations):
        super().__init__()

        self._tabs: list[ItemFrame] = []
        self.__obj = obj
        self.__backstack = []
        self.setup_tabs()
        self.fill_tabs()

        self.backbutton.bind("<Button-1>", self.back)
        self.bind("<Escape>", self.back)

    def setup_tabs(self):
        for name in self.__obj.get_relation_names():
            frame = ItemFrame(self._tab_control)
            frame.add_listener(self)
            self._tabs.append(frame)
            self._tabs[-1].grid(row=0, column=0, sticky='nsew')
            self._tab_control.add(self._tabs[-1], text=name)

    def fill_tabs(self):
        for i in range(len(self._tabs)):
            self._tabs[i].setup(self.__obj.get_relation_classes()[i], 750, self.__obj.get_relation_data()[i])
