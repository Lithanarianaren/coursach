from tkinter import Tk, ttk, Frame

from gui.event.Event import Event
from gui.event.Listener import Listener


class WindowLayout(Tk):

    def __init__(self):
        super().__init__()
        #self.eval('tk::PlaceWindow . center')
        self.minsize(600,400)
        self.geometry('1200x800')
        self.object_desc=ttk.Frame(self, padding="10", relief='groove')
        self.object_desc.place(anchor='nw', relwidth=1, relheight=0.2, x=10, y=10, width=-20, height=-20)
        self.backbutton=ttk.Button(self,text='Назад')
        self.backbutton.place(anchor='nw',width=50,height=25,x=15,y=15)
        self._tab_control = ttk.Notebook(self)
        self._tab_control.place(anchor='nw',x=10,y=0,relwidth=1,relheight=0.8,rely=0.2,width=-20,height=-10)
        #self._tab_control.pack(expand=1, fill='both')


