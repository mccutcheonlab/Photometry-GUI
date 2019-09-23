# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 07:00:14 2018
Photometry GUI to extract TDT files and view events and data
@author: jaimeHP
"""
# Import statements
import sys
#sys.path.append('C:\\Github\\functions-and-figures\\')
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import string
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import ntpath
import csv
import collections
import tdt
import scipy.signal as sig

#import JM_general_functions as jmf
#import JM_custom_figs as jmfig

import photogui_fx

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

        self.processBtn = ttk.Button(self, text='Process Signals', command=self.processdata)
        self.choosefileBtn = ttk.Button(self, text='Choose File', command=self.choosefile)
        self.makesnipsBtn = ttk.Button(self, text='Make Snips', command=self.makesnips)
        self.makelickrunsBtn = ttk.Button(self, text='Lick runs', command=self.makelickruns)
        self.loaddataBtn = ttk.Button(self, text='Load data', command=self.loaddata)
        
        self.shortfilename = StringVar(self.master)
        self.shortfilename.set('No file chosen')
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

        self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=200, mode='determinate')

        self.aboutLbl = ttk.Label(self, text='Photometry Analyzer-2.0 by J McCutcheon')
# Packing grid with widgets
        
        self.f2.grid(column=2, row=0, columnspan=8, rowspan=3, sticky=(N,S,E,W))
        self.f3.grid(column=0, row=4, columnspan=4, sticky=(N,S,E,W))
        self.f4.grid(column=4, row=4, columnspan=4, sticky=(N,S,E,W))
        
        self.processBtn.grid(column=0, row=0)
        self.choosefileBtn.grid(column=0, row=1)
        self.filenameLbl.grid(column=0, row=2, columnspan=2, sticky=W)
        
        self.loaddataBtn.grid(column=1, row=0)
        
        self.baselineLbl.grid(column=0, row=3, sticky=E)
        self.baselineField.grid(column=1, row=3)
        self.snipitLbl.grid(column=2, row=3, sticky=E)
        self.snipitField.grid(column=3, row=3)
        self.nbinsLbl.grid(column=4, row=3, sticky=E)
        self.nbinsField.grid(column=5, row=3)
        
        self.makesnipsBtn.grid(column=9, row=3, sticky=(W,E))
        self.makelickrunsBtn.grid(column=8, row=4, columnspan=2)

        self.aboutLbl.grid(column=0, row=5, columnspan=3, sticky=W)
        self.progress.grid(column=0, row=6)
     
        self.blue = StringVar(self.master)       
        self.uv = StringVar(self.master)  
        self.eventsVar = StringVar(self.master)
        self.onsetVar = StringVar(self.master)
        self.licksVar = StringVar(self.master)
        self.updatesigoptions()
        self.updateeventoptions()
        
        self.sessionviewer()
        
    def choosefile(self):
        # open window to choose file
        #self.tdtfile = filedialog.askopenfilename(initialdir=currdir, title='Select a file.')
        self.tdtfile = 'C:\\Github\\PPP_analysis\\data\\Eelke-171027-111329\\'
        self.shortfilename.set(ntpath.basename(self.tdtfile))
        
        # opens file to get stream and epoch names
        self.getstreamandepochnames()
        
        # set tick
        self.setticks()
        
        # update dropdown menu options
        self.updatesigoptions()
        self.updateeventoptions()
    
    def getstreamandepochnames(self):
        tmp = tdt.read_block(self.tdtfile, t2=2, evtype=['streams'])
        self.streamfields = [v for v in vars(tmp.streams) if v != 'Fi2r']
        
        tmp = tdt.read_block(self.tdtfile, evtype=['epocs'])
        self.epocs = getattr(tmp, 'epocs')
        self.epochfields = [v for v in vars(self.epocs)]
        
    def setticks(self):
        try:
            self.tick = self.epocs.Tick['onset']
            print('Ticks set.')
            return
        except: print('Could not assign tick automatically')
        
    def updatesigoptions(self):
        try:
            sigOptions = self.streamfields
        except AttributeError:
            sigOptions = ['None']
            
        self.chooseblueMenu = ttk.OptionMenu(self, self.blue, *sigOptions)
        self.chooseuvMenu = ttk.OptionMenu(self, self.uv, *sigOptions)
        
        self.chooseblueMenu.grid(column=1, row=1)
        self.chooseuvMenu.grid(column=1, row=2)

    def updateeventoptions(self):
        try:
            eventOptions = self.epochfields
            lickOptions = self.epochfields
        except AttributeError:
            eventOptions = ['None']
            lickOptions = ['None']
        
        self.chooseeventMenu = ttk.OptionMenu(self, self.eventsVar, *eventOptions)
        self.chooseeventMenu.grid(column=6, row=3)
        
        onsetOptions = ['onset', 'offset']
        self.onsetMenu = ttk.OptionMenu(self, self.onsetVar, *onsetOptions)
        self.onsetMenu.grid(column=7, row=3)

        self.chooselicksMenu = ttk.OptionMenu(self, self.licksVar, *lickOptions)
        self.chooselicksMenu.grid(column=8, row=3)
        
    def loaddata(self):
        # load in streams
        self.loadstreams()
        
        # process data
        self.processdata()
        
        # plot all session data
        self.sessionviewer()
        
    def loadstreams(self):       
        try:
            tmp = tdt.read_block(self.tdtfile, evtype=['streams'], store=self.blue.get())
            self.data = getattr(tmp.streams, self.blue.get())['data']
            self.fs = getattr(tmp.streams, self.blue.get())['fs']
            
            tmp = tdt.read_block(self.tdtfile, evtype=['streams'], store=self.uv.get())
            self.datauv = getattr(tmp.streams, self.uv.get())['data']
        except:
            print('No file chosen yet or problem extracting signals')
    
    def processdata(self):
        pt = len(self.data)
        X = np.fft.rfft(self.datauv, pt)
        Y = np.fft.rfft(self.data, pt)
        Ynet = Y-X
    
        datafilt = np.fft.irfft(Ynet)
    
        datafilt = sig.detrend(datafilt)
    
        b, a = sig.butter(9, 0.012, 'low', analog=True)
        self.datafilt = sig.filtfilt(b, a, datafilt)
        
    def sessionviewer(self):
        f = Figure(figsize=(7,2))
        ax = f.subplots(ncols=2)

        try:
            ax[0].plot(self.data, color='blue')
        except AttributeError: pass
        try:
            ax[0].plot(self.datauv, color='m')
        except AttributeError: pass
    
        try:
            ax[1].plot(self.datafilt, color='g')
        except: pass
        
        for axis in ax:
            try:
                axis.set_xticks(np.multiply([0, 10, 20, 30, 40, 50, 60],60*self.fs))
                axis.set_xticklabels(['0', '10', '20', '30', '40', '50', '60'])
                axis.set_xlabel('Time (min)')        
            except: pass
#        try:
#            combined = np.concatenate((self.data, self.datauv), axis=0)
#            upper = jmf.findpercentilevalue(combined, 0.95)
#            lower = jmf.findpercentilevalue(combined, 0.05)
#            ax[1].set_ylim([lower, upper])
#        except: print('Getting y-axis limits for session viewer is not working')
        
#        try:
#            for i, x in enumerate(self.epochfields):
#                print(i, x)
##                onset = getattr(output, x).onset * self.fs
##                ax[0].scatter(onset, [i]*len(onset))
#        except:
#            print('could not plot events')
#            pass
        
        canvas = FigureCanvasTkAgg(f, self.f2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))

    def makesnips(self):
        # get events and number of bins from dropdown menus
        self.setevents()
        self.bins = int(self.nbins.get())
        
        # extract snips and calculate noise from data
        self.time2samples()
        self.randomevents = makerandomevents(120, max(self.tick)-120)
        self.bgTrials, self.pps = snipper(self.data, self.randomevents,
                                        t2sMap = self.t2sMap, fs = self.fs, bins=self.bins)
        self.snips = mastersnipper(self, self.events)
        self.getnoiseindex()
        
        # plot data
        self.singletrialviewer()
        self.averagesnipsviewer()
        
    def setevents(self):
        try:
            if self.eventsVar.get() == 'runs':
                self.events = self.runs
            else:
                self.eventepoc = getattr(self.epocs, self.eventsVar.get())
                self.events = getattr(self.eventepoc, self.onsetVar.get())

            self.lickepoc = getattr(self.epocs, self.licksVar.get())
            self.licks = getattr(self.lickepoc, self.onsetVar.get())
        except:
            alert('Cannot set event')

    def getnoiseindex(self):
        self.noisemethod = 'sum'
        self.threshold = 8
        bgMAD = findnoise(self.data, self.randomevents,
                              t2sMap = self.t2sMap, fs = self.fs, bins=self.bins,
                              method=self.noisemethod)          
        sigSum = [np.sum(abs(i)) for i in self.snips['blue']]
        sigSD = [np.std(i) for i in self.snips['blue']]
        self.noiseindex = [i > bgMAD*self.threshold for i in sigSum]

    def makelickruns(self):
        self.setevents()
        # need to set lick runs as if a normal output variable
        self.runs = [val for i, val in enumerate(self.licks) if (val - self.licks[i-1] > 10)]
        self.epochfields.append('runs')
        self.updateeventoptions()

    def singletrialviewer(self):
        f = Figure(figsize=(3,2)) # 5,3
        ax = f.add_subplot(111)
        
        jmfig.trialsFig(ax, self.snips['blue'], noiseindex=self.noiseindex)
        
        alltrialVar = StringVar(self.f3)
        ttk.Radiobutton(self.f3, text='All Trials', variable=alltrialVar, value='all').grid(
                row=0, column=1)
        ttk.Radiobutton(self.f3, text='Single Trial', variable=alltrialVar, value='single').grid(
                row=1, column=1)

        currenttrialVar = IntVar(self.f3)
        currenttrialVar.set(0)
        self.trialEntry = ttk.Entry(self.f3, textvariable=currenttrialVar).grid(
                row=1, column=2)
     
        canvas = FigureCanvasTkAgg(f, self.f3)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))
        
    def averagesnipsviewer(self):
        self.progress.start()
        f = Figure(figsize=(5,2)) # 5.3
        ax = f.add_subplot(111)
        
        jmfig.trialsMultShadedFig(ax, [self.snips['uv'], self.snips['blue']],
                          self.pps,
                          eventText = self.eventsVar.get())
        
        canvas = FigureCanvasTkAgg(f, self.f4)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))
        self.progress.stop()

    def time2samples(self):
        maxsamples = len(self.tick)*int(self.fs)
        if (len(self.data) - maxsamples) > 2*int(self.fs):
            print('Something may be wrong with conversion from time to samples')
            print(str(len(self.data) - maxsamples) + ' samples left over. This is more than double fs.')
            self.t2sMap = np.linspace(min(self.tick), max(self.tick), maxsamples)
        else:
            self.t2sMap = np.linspace(min(self.tick), max(self.tick), maxsamples)
            
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

def snipper(data, timelock, fs = 1, t2sMap = [], preTrial=10, trialLength=30,
                 adjustBaseline = True,
                 bins = 0):

    if len(timelock) == 0:
        print('No events to analyse! Quitting function.')
        raise Exception('no events')

    pps = int(fs) # points per sample
    pre = int(preTrial*pps) 
#    preABS = preTrial
    length = int(trialLength*pps)
# converts events into sample numbers
    event=[]
    if len(t2sMap) > 1:
        for x in timelock:
            event.append(np.searchsorted(t2sMap, x, side="left"))
    else:
        event = [x*fs for x in timelock]

    new_events = []
    for x in event:
        if int(x-pre) > 0:
            new_events.append(x)
    event = new_events

    nSnips = len(event)
    snips = np.empty([nSnips,length])
    avgBaseline = []

    for i, x in enumerate(event):
        start = int(x) - pre
        avgBaseline.append(np.mean(data[start : start + pre]))
        try:
            snips[i] = data[start : start+length]
        except ValueError: # Deals with recording arrays that do not have a full final trial
            snips = snips[:-1]
            avgBaseline = avgBaseline[:-1]
            nSnips = nSnips-1

    if adjustBaseline == True:
        snips = np.subtract(snips.transpose(), avgBaseline).transpose()
        snips = np.divide(snips.transpose(), avgBaseline).transpose()

    if bins > 0:
        if length % bins != 0:
            snips = snips[:,:-(length % bins)]
        totaltime = snips.shape[1] / int(fs)
        snips = np.mean(snips.reshape(nSnips,bins,-1), axis=2)
        pps = bins/totaltime
              
    return snips, pps

def mastersnipper(x, events,
                  bins=300,
                  preTrial=10,
                  trialLength=30,
                  threshold=10,
                  peak_between_time=[0, 1],
                  output_as_dict=True,
                  latency_events=[],
                  latency_direction='pre'):
    if len(events) < 1:
        print('Cannot find any events. All outputs will be empty.')
        blueTrials, uvTrials, noiseindex, diffTrials, peak, latency = ([] for i in range(5))
    else:
        blueTrials,_ = snipper(x.data, events,
                                   t2sMap=x.t2sMap,
                                   fs=x.fs,
                                   bins=bins,
                                   preTrial=preTrial,
                                   trialLength=trialLength)
        uvTrials,_ = snipper(x.datauv, events,
                                   t2sMap=x.t2sMap,
                                   fs=x.fs,
                                   bins=bins,
                                   preTrial=preTrial,
                                   trialLength=trialLength)
        filtTrials,_ = snipper(x.datafilt, events,
                                   t2sMap=x.t2sMap,
                                   fs=x.fs,
                                   bins=bins,
                                   preTrial=preTrial,
                                   trialLength=trialLength,
                                   adjustBaseline = False)
        
        filtTrials_z = zscore(filtTrials)
        
        bgMAD = findnoise(x.data, x.randomevents,
                              t2sMap=x.t2sMap, fs=x.fs, bins=bins,
                              method='sum')        
        sigSum = [np.sum(abs(i)) for i in blueTrials]
        sigSD = [np.std(i) for i in blueTrials]
        noiseindex = [i > bgMAD*threshold for i in sigSum]

        output = {}
        output['blue'] = blueTrials
        output['uv'] = uvTrials
        output['filt'] = filtTrials
        output['filtz'] = filtTrials_z
        output['noise'] = noiseindex
        
        return output

def zscore(snips, baseline_points=100):
    
    BL_range = range(baseline_points)
    z_snips = []
    for i in snips:
        mean = np.mean(i[BL_range])
        sd = np.std(i[BL_range])
        z_snips.append([(x-mean)/sd for x in i])
        
    return z_snips

def findnoise(data, background, t2sMap = [], fs = 1, bins=0, method='sd'):
    
    bgSnips, _ = snipper(data, background, t2sMap=t2sMap, fs=fs, bins=bins)
    
    if method == 'sum':
        bgSum = [np.sum(abs(i)) for i in bgSnips]
        bgMAD = med_abs_dev(bgSum)
    elif method == 'sd':
        bgSD = [np.std(i) for i in bgSnips]
        bgMAD = med_abs_dev(bgSD)
   
    return(bgMAD)

def removenoise(snipsIn, noiseindex):
    snipsOut = np.array([x for (x,v) in zip(snipsIn, noiseindex) if not v])   
    return snipsOut

def med_abs_dev(data, b=1.4826):
    median = np.median(data)
    devs = [abs(i-median) for i in data]
    mad = np.median(devs)*b
                   
    return mad

root = Tk()

currdir = os.getcwd()
currdir = 'C:\\Users\\jaimeHP\\Documents\\Test Data\\'

app = Window(root)
root.lift()
root.mainloop()