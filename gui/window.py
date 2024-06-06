from gui.widgets.Window import Window
from classes import *


#здесь я эксперементировал, вроде все работает

sevStore = System()

item1 = Item("yoburt", 10, 100)
item2 = Item("tvogor", 20, 399)

store1 = Store("RUSSIA", 'zhopa', 'bear-avenu', '12', 500)

tr1 = Transaction(store1, True, 'pervaya pokupka', False, [item1, item2], 499)

store1.add_transaction(tr1)

store1.complete_monetary_transaction(tr1)

vasya = Worker(5, 'Vasya', 300, "+79556439911")
store1.add_relation(vasya)

sevStore.add_relation(store1)


WHammmer40000 = Warehouse('Kazakhstan', 'Shaurma-city', 'Plov-avenu', 15)

store1.transfer_items([item1], WHammmer40000)

sevStore.add_relation(WHammmer40000)



import json
j = sevStore.get_json()
print(json.dumps(j, indent=4))
print(store1.str_address())
from bd.jsonSaveLoad import *

SavingJSON.save_system(sevStore)
sys = LoadJSON.load_system()
print(json.dumps(sys.get_json(), indent=4))
#
#
# w=Window(sevStore)
# from gui import styles
# w.mainloop()
#
#
