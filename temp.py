

from tkinter import *
from tkinter import ttk

class Window(Frame):
    
    def __init__(self, master=None):
        # f1 = ttk.Style()
        # f1.configure('.', background='powder blue', padding=5)
        # f2 = ttk.Style()
        # f2.configure('inner.TFrame', background='light cyan')
        
        ttk.Frame.__init__(self, master, style='TFrame', padding=(10, 10, 15, 15))
        self.master = master        
        self.init_window()

    def init_window(self):
        self.master.title('Test window')
        self.pack(fill=BOTH, expand=1)

        self.f2 = ttk.Frame(self, style='inner.TFrame', relief='sunken',
                            borderwidth=5, height=150)
        self.f3 = ttk.Frame(self, style='inner.TFrame', relief='sunken',
                            borderwidth=5, height=200, width=400)


        self.testLbl = ttk.Label(self.f2, text='Hey there')
        self.test2Lbl = ttk.Label(self.f3, text='Whassup?')

        self.stopBtn = ttk.Button(self.f3, text='Stop!', command=self.stop_pb)
        self.pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")


        self.f2.grid(column=0, row=0, sticky=(N,S,E,W))
        self.f3.grid(column=1, row=1, sticky=(N,S,E,W))
        self.pb.grid(column=0, row=3)


        self.testLbl.grid(column=2, row=2)
        self.stopBtn.grid(column=0, row=0)

        self.pb.start()

    def stop_pb(self):
        self.pb.stop()



root = Tk()

app = Window(root)
root.lift()
root.mainloop()