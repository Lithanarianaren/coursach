from gui.widgets.Window import Window
from classes import *


sevStore = System()
# sevStore.accept_transaction(sevStore.active_trans[0])

# sevStore.sell_items([Item("moloko", 90)])



w=Window(sevStore)
print(0)
from gui import styles
w.mainloop()