# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 07:00:14 2018
Photometry GUI to extract TDT files and view events and data
@author: jaimeHP
"""
# Import statements
import sys
sys.path.append('C:\\Users\\jaimeHP\\Documents\\GitHub\\functions-and-figures\\')
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

import JM_general_functions as jmf
import JM_custom_figs as jmfig

# Main class for GUI
class Window(Frame):
    
    def __init__(self, master=None):
        f1 = ttk.Style()
        f1.configure('.', background='powder blue', padding=5)
        f1.configure('TButton', width=15, sticky=(E,W))
        f1.configure('TEntry', width=10)
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
        self.viewsessionBtn = ttk.Button(self, text='View Session', command=self.sessionviewer)
        
        self.shortfilename = StringVar(self.master)
        self.shortfilename.set('No file loaded')
        self.filenameLbl = ttk.Label(self, textvariable=self.shortfilename)
        
        self.baselineLbl = ttk.Label(self, text='Baseline (s)')
        self.snipitLbl = ttk.Label(self, text='Snipit length (s)')
        self.nbinsLbl = ttk.Label(self, text='No. of bins')
#        self.chooseeventLbl = ttk.Label(self, text='Choose event')
        
        self.baseline = StringVar(self.master)
        self.baselineField = ttk.Entry(self, textvariable=self.baseline)
        self.baselineField.insert(END, '10')

        self.snipitlength = StringVar(self.master)
        self.snipitField = ttk.Entry(self, textvariable=self.snipitlength)
        self.snipitField.insert(END, '30')
        
        self.nbins = StringVar(self.master)
        self.nbinsField = ttk.Entry(self, textvariable=self.nbins)
        self.nbinsField.insert(END, '300')

        self.snipsprogress = ttk.Progressbar(self, orient=VERTICAL, length=200, mode='determinate')
       
        self.aboutLbl = ttk.Label(self, text='Photometry Analyzer-1.0 by J McCutcheon')
# Packing grid with widgets
        
        self.f2.grid(column=2, row=0, columnspan=8, rowspan=3, sticky=(N,S,E,W))
        self.f3.grid(column=0, row=4, columnspan=4, sticky=(N,S,E,W))
        self.f4.grid(column=4, row=4, columnspan=4, sticky=(N,S,E,W))
        
        self.converttdtBtn.grid(column=0, row=0)
        self.loadfileBtn.grid(column=0, row=1)
        self.filenameLbl.grid(column=0, row=2, columnspan=2, sticky=W)
        
        self.viewsessionBtn.grid(column=1, row=0)
        
        self.baselineLbl.grid(column=0, row=3, sticky=E)
        self.baselineField.grid(column=1, row=3)
        self.snipitLbl.grid(column=2, row=3, sticky=E)
        self.snipitField.grid(column=3, row=3)
        self.nbinsLbl.grid(column=4, row=3, sticky=E)
        self.nbinsField.grid(column=5, row=3)
        
        self.makesnipsBtn.grid(column=8, row=3, columnspan=2, sticky=(W,E))
        self.snipsprogress.grid(column=8, row=4, columnspan=2)

        self.aboutLbl.grid(column=0, row=5, columnspan=3, sticky=W)
     
        self.blue = StringVar(self.master)       
        self.uv = StringVar(self.master)  
        self.eventsVar = StringVar(self.master)
        self.onsetVar = StringVar(self.master)
        self.updatesigoptions()
        self.updateeventoptions()
        
        self.sessionviewer()
        
    def converttdt(self):
        alert('Feature coming soon!')
        
    def loadfile(self):
#        self.filename = filedialog.askopenfilename(initialdir=currdir, title='Select a file.')
        self.filename = 'C:\\Users\\jaimeHP\\Documents\\Test Data\\thph2.3thph2.4distraction.mat'
        self.shortfilename.set(ntpath.basename(self.filename))
        self.openmatfile()
    
    def openmatfile(self):
        a = sio.loadmat(self.filename, squeeze_me=True, struct_as_record=False) 
        self.output = a['output']
        self.fs = self.output.fs1
        self.getstreamfields()
        self.getepochfields()
        self.updatesigoptions()
       
    def makesnips(self):
        self.snipsprogress.start()
        self.setevents()
        self.bins = int(self.nbins.get())
        self.time2samples()
        self.randomevents = makerandomevents(120, max(self.output.Tick.onset)-120)
        self.bgTrials, self.pps = jmf.snipper(self.data, self.randomevents,
                                        t2sMap = self.t2sMap, fs = self.fs, bins=self.bins)
        self.snips = jmf.mastersnipper(self, self.events)
        self.getnoiseindex()
        self.singletrialviewer()
        self.averagesnipsviewer()
        self.snipsprogress.stop()
    
    def getnoiseindex(self):
        self.noisemethod = 'sum'
        self.threshold = 8
        bgMAD = jmf.findnoise(self.data, self.randomevents,
                              t2sMap = self.t2sMap, fs = self.fs, bins=self.bins,
                              method=self.noisemethod)          
        sigSum = [np.sum(abs(i)) for i in self.snips['blue']]
        sigSD = [np.std(i) for i in self.snips['blue']]
        self.noiseindex = [i > bgMAD*self.threshold for i in sigSum]
        
    def getstreamfields(self):
        self.streamfields = []
        for x in self.output._fieldnames:
            try:
                len(getattr(self.output, x))
                self.streamfields.append(x)
            except: pass
            
    def getepochfields(self):
        self.epochfields = []
        for x in self.output._fieldnames:
            var = getattr(self.output, x)
            if hasattr(var, 'onset'):
                self.epochfields.append(x)
        
    def updatesigoptions(self):
        try:
            sigOptions = self.streamfields
        except AttributeError:
            sigOptions = ['None']
            
        self.chooseblueMenu = ttk.OptionMenu(self, self.blue, *sigOptions)
        self.chooseuvMenu = ttk.OptionMenu(self, self.uv, *sigOptions)
        
        self.chooseblueMenu.grid(column=1, row=1)
        self.chooseuvMenu.grid(column=1, row=2)

    def setsignals(self):       
        try:
            self.data = getattr(self.output, self.blue.get())
            self.dataUV = getattr(self.output, self.uv.get())
        except AttributeError: pass
    
    def updateeventoptions(self):
        try:
            eventOptions = self.epochfields
        except AttributeError:
            eventOptions = ['None']
        
        self.chooseeventMenu = ttk.OptionMenu(self, self.eventsVar, *eventOptions)
        self.chooseeventMenu.grid(column=6, row=3)
        
        onsetOptions = ['onset', 'offset']
        self.onsetMenu = ttk.OptionMenu(self, self.onsetVar, *onsetOptions)
        self.onsetMenu.grid(column=7, row=3)
    
    def setevents(self):
        try:
            self.event = getattr(self.output, self.eventsVar.get())
            self.events = getattr(self.event, self.onsetVar.get())
        except: pass
        
    def sessionviewer(self):
        self.updateeventoptions()
        self.setsignals()

        f = Figure(figsize=(7,2))
        ax = f.add_subplot(111)
        try:
            ax.plot(self.data, color='blue')
        except AttributeError: pass
        try:
            ax.plot(self.dataUV, color='m')
        except AttributeError: pass
        try:
            ax.set_xticks(np.multiply([0, 10, 20, 30, 40, 50, 60],60*self.fs))
            ax.set_xticklabels(['0', '10', '20', '30', '40', '50', '60'])
            ax.set_xlabel('Time (min)')        
        except: pass
        
        canvas = FigureCanvasTkAgg(f, self.f2)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))
        
    def singletrialviewer(self):
        f = Figure(figsize=(3,2)) # 5,3
        ax = f.add_subplot(111)
        
        jmfig.trialsFig(ax, self.snips['blue'], noiseindex=self.noiseindex)
        
        alltrialVar = StringVar(self.f3)
        ttk.Radiobutton(self.f3, text='All Trials', variable=alltrialVar, value='all').grid(
                row=0, column=0)
        ttk.Radiobutton(self.f3, text='Single Trial', variable=alltrialVar, value='single').grid(
                row=0, column=1)
        
        
        
        currenttrialVar = IntVar(self.f3)
        currenttrialVar.set(0)
        self.trialEntry = ttk.Entry(self.f3, textvariable=currenttrialVar).grid(
                row=0, column=2)

#                
#        
#        canvas = FigureCanvasTkAgg(f, self.f3)
#        canvas.show()
#        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))
        
    def averagesnipsviewer(self):
        f = Figure(figsize=(5,2)) # 5.3
        ax = f.add_subplot(111)
        
        jmfig.trialsMultShadedFig(ax, [self.snips['uv'], self.snips['blue']],
                          self.pps,
                          eventText = self.eventsVar.get())
        
        canvas = FigureCanvasTkAgg(f, self.f4)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))

    def time2samples(self):
        tick = self.output.Tick.onset
        maxsamples = len(tick)*int(self.fs)
        if (len(self.data) - maxsamples) > 2*int(self.fs):
            print('Something may be wrong with conversion from time to samples')
            print(str(len(self.data) - maxsamples) + ' samples left over. This is more than double fs.')
            self.t2sMap = np.linspace(min(tick), max(tick), maxsamples)
        else:
            self.t2sMap = np.linspace(min(tick), max(tick), maxsamples)
            
    def event2sample(self, EOI):
        idx = (np.abs(self.t2sMap - EOI)).argmin()   
        return idx
       
def alert(msg):
    print(msg)
    messagebox.showinfo('Error', msg)
    
def makerandomevents(minTime, maxTime, spacing = 77, n=100):
    events = []
    total = maxTime-minTime
    start = 0
    for i in np.arange(0,n):
        if start > total:
            start = start - total
        events.append(start)
        start = start + spacing
    events = [i+minTime for i in events]
    return events

root = Tk()

currdir = os.getcwd()
currdir = 'C:\\Users\\jaimeHP\\Documents\\Test Data\\'

app = Window(root)
root.lift()
root.mainloop()