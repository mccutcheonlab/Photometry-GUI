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
        
        ttk.Frame.__init__(self, master, style='TFrame', padding=(10, 10, 15, 15))               
        self.master = master
        
        self.init_window()

    def init_window(self):
        self.master.title('Photometry Analyzer')
        self.pack(fill=BOTH, expand=1)

root = Tk()

currdir = os.getcwd()
currdir = 'C:\\Users\\jaimeHP\\Dropbox\\Python\\cas9\\cas9_medfiles\\'

app = Window(root)
root.lift()
root.mainloop()