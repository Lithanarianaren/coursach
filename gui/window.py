from gui.widgets.Window import Window
from classes import  *

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
# whSev.fire(wrk)

# del_items
tr = Transaction([item1, item2], "транзация")
tr.del_items([Item("sapog")])
whSev.del_items([Item("moloko")])

# del_transaction
whSev.add_transaction(tr)
whSev.del_transaction(tr)

# sell_items & buy_items
sevStore = Store(1, 3000)
sevStore.buy_items([item1])
# sevStore.accept_transaction(sevStore.active_trans[0])

# sevStore.sell_items([Item("moloko", 90)])

# get_salary
wrk.salary += 300
wrk.get_salary(sevStore)

w=Window(sevStore)
print(0)
from gui import styles
w.mainloop()