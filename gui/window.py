from bd.jsonSaveLoad import *
from gui.widgets.Window import Window
from classes import *

sys = LoadJSON.load_system()


w=Window(sys)
from gui import styles
w.mainloop()


