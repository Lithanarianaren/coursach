from tkinter import Tk, ttk

from classes import *
from gui.relation.HasInternalRelations import HasInternalRelations
from gui.relation.Relation import Relation


class Window(Tk):

    TABLE_WIDTH=750

    def __init__(self, obj: HasInternalRelations):
        super().__init__()

        self._relations:list[Relation]=[]
        self._tab_control = ttk.Notebook(self)
        self._tab_control.grid(row=0,column=0,sticky='nsew')
        self._tabs:list[ttk.Frame] = []
        self.__obj = obj
        self.resizable(height=False, width=False)
        self.eval('tk::PlaceWindow . center')
        # print(s.role, type(s.role))
        self.title("Кабинет администратора")
        self.geometry('800x400')
        self.setup_tabs()
        self.fill_tabs()

    def setup_tabs(self):
        for name in self.__obj.get_relation_names():
            self._tabs.append(ttk.Frame(self._tab_control))
            self._tabs[-1].grid(row=0,column=0,sticky='nsew')
            self._tab_control.add(self._tabs[-1],text=name)
        self._tab_control.pack(expand=1, fill='both')

    def fill_tabs(self):
        for i in range(len(self._tabs)):
            rel=Relation(self._tabs[i],self.__obj.get_relation_classes()[i],750)
            rel.set_data(self.__obj.get_relation_data()[i])
            rel.show_data()
            rel.position()
            self._relations.append(rel)



# тесты, чекать по желанию
item1 = Item("moloko", 100, 3)
item2 = Item("sapog", 1000, 13)
item3 = Item("karandash", 35, 50)

wh1 = Warehouse()
wh1.id = 1
wh1.add_items([item1, item2])

whSev = Warehouse()
whSev.id = 2
whSev.add_items([item3])

# count_cost
tr1 = Transaction([item1, item3], "new purchase")



# transfer_items & add_transaction & accept_transaction & add_items
itemToTrans = Item("moloko", 100, 2)
wh1.transfer_items([itemToTrans], whSev)
whSev.accept_transaction(whSev.active_trans[0])

# hire и fire
wrk = Worker(1, "loh", 350, "88005553555")
whSev.hire(wrk)
whSev.fire(wrk)

# del_items
tr = Transaction([item1, item2])
tr.del_items([Item("sapog")])
whSev.del_items([Item("moloko")])



# del_transaction
whSev.add_transaction(tr)
whSev.del_transaction(tr)

# sell_items & buy_items
sevStore = Store(1, 3000)
sevStore.buy_items([item1])
sevStore.accept_transaction(sevStore.active_trans[0])



sevStore.sell_items([Item("moloko", 90)])



# get_salary
wrk.salary += 300
wrk.get_salary(sevStore)





Window(sevStore).mainloop()