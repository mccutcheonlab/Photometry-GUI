# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 07:00:14 2018
Photometry GUI to extract TDT files and view events and data
@author: jaimeHP
"""
# Import statements
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import string
import numpy as np
import scipy.io as sio
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import ntpath#
import csv
import collections

# Main class for GUI
class Window(Frame):
    
    def __init__(self, master=None):
        f1 = ttk.Style()
        f1.configure('.', background='powder blue', padding=5)
        f1.configure('TButton', width=15, sticky=(E,W))
        f2 = ttk.Style()
        f2.configure('inner.TFrame', background='light cyan')
        
        ttk.Frame.__init__(self, master, style='TFrame', padding=(10, 10, 15, 15))               
        
        self.master = master        
        self.init_window()

    def init_window(self):
        self.master.title('Photometry Analyzer')
        self.pack(fill=BOTH, expand=1)
        
        #Frames for session window and snipits
        self.f2 = ttk.Frame(self, style='inner.TFrame', relief='sunken',
                            borderwidth=5, height=150)
        self.f3 = ttk.Frame(self, style='inner.TFrame', relief='sunken',
                            borderwidth=5, height=200, width=400)
        self.f4 = ttk.Frame(self, style='inner.TFrame', relief='sunken',
                            borderwidth=5, height=200, width=400)

        self.converttdtBtn = ttk.Button(self, text='Convert TDT File', command=self.converttdt)
        self.loadfileBtn = ttk.Button(self, text='Load File', command=self.loadfile)
        self.makesnipsBtn = ttk.Button(self, text='Make Snips', command=self.makesnips)
        
        self.shortfilename = StringVar(self.master)
        self.shortfilename.set('No file loaded')
        self.filenameLbl = ttk.Label(self, textvariable=self.shortfilename)
        
        self.baselineLbl = ttk.Label(self, text='Baseline (s)')
        self.snipitLbl = ttk.Label(self, text='Snipit length (s)')
        self.nbinsLbl = ttk.Label(self, text='No. of bins')
        
        self.baseline = StringVar(self.master)
        self.baselineField = ttk.Entry(self, textvariable=self.baseline)
        self.baselineField.insert(END, '10')

        self.snipitlength = StringVar(self.master)
        self.snipitField = ttk.Entry(self, textvariable=self.snipitlength)
        self.snipitField.insert(END, '30')
        
        self.nbins = StringVar(self.master)
        self.nbinsField = ttk.Entry(self, textvariable=self.nbins)
        self.nbinsField.insert(END, '300')
       
        self.aboutLbl = ttk.Label(self, text='Photometry Analyzer-1.0 by J McCutcheon')
# Packing grid with widgets
        
        self.f2.grid(column=2, row=0, columnspan=6, rowspan=3, sticky=(N,S,E,W))
        self.f3.grid(column=0, row=4, columnspan=4, sticky=(N,S,E,W))
        self.f4.grid(column=4, row=4, columnspan=4, sticky=(N,S,E,W))
        
        self.converttdtBtn.grid(column=0, row=0)
        self.loadfileBtn.grid(column=0, row=1)
        self.filenameLbl.grid(column=0, row=2, columnspan=2, sticky=W)
        
        self.baselineLbl.grid(column=0, row=3, sticky=E)
        self.baselineField.grid(column=1, row=3)
        self.snipitLbl.grid(column=2, row=3, sticky=E)
        self.snipitField.grid(column=3, row=3)
        self.nbinsLbl.grid(column=4, row=3, sticky=E)
        self.nbinsField.grid(column=5, row=3)
        
        self.makesnipsBtn.grid(column=6, row=3, columnspan=2, sticky=(W,E))
        
        self.aboutLbl.grid(column=0, row=5, columnspan=3, sticky=W)
        
        self.sessionviewer()
        
    def converttdt(self):
        alert('Feature coming soon!')
    def loadfile(self):
        #self.filename = filedialog.askopenfilename(initialdir=currdir, title='Select a file.')
        self.filename = 'C:\\Users\\jaimeHP\\Documents\\Test Data\\thph2.3thph2.4distraction.mat'
        self.shortfilename.set(ntpath.basename(self.filename))
        self.openmatfile()
    
    def openmatfile(self):
        a = sio.loadmat(self.filename, squeeze_me=True, struct_as_record=False) 
        self.output = a['output']
        self.fs = self.output.fs1
        self.data = self.output.result1
        self.dataUV = self.output.resultUV1
        self.sessionviewer()
        
    def sessionviewer(self):        
        f = Figure(figsize=(9,3))
        ax = f.add_subplot(111)
        try:
            ax.plot(self.data, color='blue')
            ax.plot(self.dataUV, color='m')
        
            ax.set_xticks(np.multiply([0, 10, 20, 30, 40, 50, 60],60*self.fs))
            ax.set_xticklabels(['0', '10', '20', '30', '40', '50', '60'])
            ax.set_xlabel('Time (min)')        
        except:
            pass
        
        canvas = FigureCanvasTkAgg(f, self.f2)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))
   
    def makesnips(self):
        alert('Feature coming soon!')
        
        
def alert(msg):
    print(msg)
    messagebox.showinfo('Error', msg)

root = Tk()

currdir = os.getcwd()
currdir = 'C:\\Users\\jaimeHP\\Documents\\Test Data\\'

app = Window(root)
root.lift()
root.mainloop()