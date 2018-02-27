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
        
        #Frame for session window
#        self.f2 = ttk.Frame(self, style='inner.TFrame',# borderwidth=5,
#                            relief="sunken", width=300, height=500)
#        
#        self.f2.grid(self, column=0, row=2, columnspan=6, rowspan=3, sticky=(N,S,E,W))

        self.converttdtBtn = ttk.Button(self, text='Convert TDT File', command=self.converttdt)
        self.loadfileBtn = ttk.Button(self, text='Load File', command=self.loadfile)
    
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

    
    
        self.converttdtBtn.grid(column=0, row=0)
        self.loadfileBtn.grid(column=0, row=1)
        self.filenameLbl.grid(column=0, row=2, sticky=W)
        
        self.baselineLbl.grid(column=0, row=3, sticky=E)
        self.baselineField.grid(column=1, row=3)
        self.snipitLbl.grid(column=2, row=3, sticky=E)
        self.snipitField.grid(column=3, row=3)
        self.nbinsLbl.grid(column=4, row=3, sticky=E)
        self.nbinsField.grid(column=5, row=3)
        
        self.aboutLbl.grid(column=0, row=5, columnspan=3, sticky=W)
        
    def converttdt(self):
        alert('Feature coming soon!')
    def loadfile(self):
        alert('Feature coming soon!')
        
        
def alert(msg):
    print(msg)
    messagebox.showinfo('Error', msg)

root = Tk()

currdir = os.getcwd()

app = Window(root)
root.lift()
root.mainloop()