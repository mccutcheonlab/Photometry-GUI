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
                            borderwidth=5, height=150)
        self.f4 = ttk.Frame(self, style='inner.TFrame', relief='sunken',
                            borderwidth=5, height=200, width=200)
        self.f5 = ttk.Frame(self, style='inner.TFrame', relief='sunken',
                            borderwidth=5, height=200, width=200)
        self.f6 = ttk.Frame(self, style='inner.TFrame', relief='sunken',
                            borderwidth=5, height=200, width=200)

        # Button definitions
        self.choosefileBtn = ttk.Button(self, text='Choose File', command=self.choosefile)
        self.loaddataBtn = ttk.Button(self, text='Load data', command=self.loaddata)
        self.makelickrunsBtn = ttk.Button(self, text='Lick runs', command=self.makelickruns)
        self.makesnipsBtn = ttk.Button(self, text='Make Snips', command=self.makesnips)
        self.noiseBtn = ttk.Button(self, text='Turn noise off', command=self.togglenoise)
        self.prevtrialBtn = ttk.Button(self, text='Prev Trial', command=self.prevtrial)
        self.nexttrialBtn = ttk.Button(self, text='Next Trial', command=self.nexttrial)
        self.showallBtn = ttk.Button(self, text='Show All', command=self.showall)

        # Label definitions
        self.shortfilename = StringVar(self.master)
        self.shortfilename.set('No file chosen')
        self.filenameLbl = ttk.Label(self, textvariable=self.shortfilename, wraplength=200)
        
        self.baselineLbl = ttk.Label(self, text='Baseline (s)')
        self.lengthLbl = ttk.Label(self, text='Snipit length (s)')
        self.nbinsLbl = ttk.Label(self, text='No. of bins')
        self.noisethLbl = ttk.Label(self, text='Noise threshold')
        
        # Field and entries
        self.baseline = StringVar(self.master)
        self.baselineField = ttk.Entry(self, textvariable=self.baseline)
        self.baselineField.insert(END, '10')

        self.length = StringVar(self.master)
        self.lengthField = ttk.Entry(self, textvariable=self.length)
        self.lengthField.insert(END, '30')
        
        self.nbins = StringVar(self.master)
        self.nbinsField = ttk.Entry(self, textvariable=self.nbins)
        self.nbinsField.insert(END, '300')
        
        self.noiseth = StringVar(self.master)
        self.noisethField = ttk.Entry(self, textvariable=self.noiseth)
        self.noisethField.insert(END, '10')

        # Progress bar and about label
        self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=200, mode='determinate')

        self.aboutLbl = ttk.Label(self, text='Photometry Analyzer-2.0 by J McCutcheon')

        
        # Packing grid with widgets
        self.f2.grid(column=2, row=0, columnspan=3, rowspan=3, sticky=(N,S,E,W))
        self.f3.grid(column=5, row=0, columnspan=3, rowspan=3, sticky=(N,S,E,W))
        self.f4.grid(column=2, row=4, columnspan=2, rowspan=5, sticky=(N,S,E,W))
        self.f5.grid(column=4, row=4, columnspan=2, rowspan=5, sticky=(N,S,E,W))
        self.f6.grid(column=6, row=4, columnspan=2, rowspan=5, sticky=(N,S,E,W))
        
        self.choosefileBtn.grid(column=0, row=0)
        self.loaddataBtn.grid(column=0, row=1)
        self.filenameLbl.grid(column=0, row=2, columnspan=2, sticky=W)
        
        self.makelickrunsBtn.grid(column=1, row=4)
        
        self.baselineLbl.grid(column=0, row=5, sticky=E)
        self.baselineField.grid(column=1, row=5)
        self.lengthLbl.grid(column=0, row=6, sticky=E)
        self.lengthField.grid(column=1, row=6)
        self.nbinsLbl.grid(column=0, row=7, sticky=E)
        self.nbinsField.grid(column=1, row=7)
        self.noisethLbl.grid(column=0, row=8, sticky=E)
        self.noisethField.grid(column=1, row=8)
               
        self.makesnipsBtn.grid(column=9, row=4, rowspan=2, sticky=(N, S, W,E))
        self.noiseBtn.grid(column=9, row=7, sticky=(W,E))
        
        self.aboutLbl.grid(column=0, row=11, columnspan=3, sticky=W)
        self.progress.grid(column=0, row=12, columnspan=2, sticky=(W, E))
     
        self.blue = StringVar(self.master)       
        self.uv = StringVar(self.master)  
        self.eventsVar = StringVar(self.master)
        self.onsetVar = StringVar(self.master)
        self.lickrunsVar = StringVar(self.master)
        self.snipsVar = StringVar(self.master)
        self.noisethVar = IntVar(self.master)
        self.noise=True
        
        self.updatesigoptions()
        self.updateeventoptions()
        
        self.sessionviewer()
        
    def choosefile(self):
        # open window to choose file
        #self.tdtfile = filedialog.askopenfilename(initialdir=currdir, title='Select a file.')
        self.tdtfile = 'C:\\Github\\PPP_analysis\\data\\Eelke-171027-111329\\'
        self.shortfilename.set(ntpath.dirname(self.tdtfile))
        
        print(self.shortfilename.get())
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
            
        self.chooseblueMenu = ttk.OptionMenu(self, self.blue, sigOptions[0], *sigOptions)
        self.chooseuvMenu = ttk.OptionMenu(self, self.uv, sigOptions[0], *sigOptions)
        
        self.chooseblueMenu.grid(column=1, row=0)
        self.chooseuvMenu.grid(column=1, row=1)

    def updateeventoptions(self):
        try:
            eventOptions = self.epochfields
            lickrunOptions = self.epochfields
        except AttributeError:
            eventOptions = ['None']
            lickrunOptions = ['None']
        
        self.chooseeventMenu = ttk.OptionMenu(self, self.eventsVar, eventOptions[0], *eventOptions)
        self.chooseeventMenu.grid(column=0, row=3)

        snipOptions = ['blue', 'uv', 'filt', 'filt_z']
        self.choosesnipMenu = ttk.OptionMenu(self, self.snipsVar, snipOptions[0], *snipOptions)
        self.choosesnipMenu.grid(column=9, row=6)
   
        onsetOptions = ['onset', 'offset']
        self.onsetMenu = ttk.OptionMenu(self, self.onsetVar, onsetOptions[0], *onsetOptions)
        self.onsetMenu.grid(column=1, row=3)

        self.chooselicksMenu = ttk.OptionMenu(self, self.lickrunsVar, lickrunOptions[0], *lickrunOptions)
        self.chooselicksMenu.grid(column=0, row=4)
        
    def loaddata(self):   
        self.progress['value'] = 40
        # load in streams
        self.loadstreams()
        self.progress['value'] = 60
        
        # process data
        self.processdata()
        self.progress['value'] = 80
        
        # plot all session data
        self.sessionviewer()
        self.progress['value'] = 100
        
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
        # plot blue and uv signals
        fig1 = Figure(figsize=(4,2))
        ax = fig1.subplots()

        try:
            ax.plot(self.data, color='blue')
        except AttributeError: pass
        try:
            ax.plot(self.datauv, color='m')
        except AttributeError: pass

        # plot filtered signal
        fig2 = Figure(figsize=(4,2))
        ax = fig2.subplots()
    
        try:
            ax.plot(self.datafilt, color='g')
        except: pass
        
        #label axes
        for fig in [fig1, fig2]:
            try:
                ax=fig.axes[0]
                maxtime=np.ceil(ax.get_xlim()[1] / self.fs / 60)
                ax.set_xticks(np.multiply(np.arange(0, maxtime, 10),60*self.fs))
                ax.set_xticklabels(['0', '10', '20', '30', '40', '50', '60'])
                ax.set_xlabel('Time (min)')        
            except: pass
        
        #add figures to frames
        canvas = FigureCanvasTkAgg(fig1, self.f2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))
        
        canvas = FigureCanvasTkAgg(fig2, self.f3)
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
        self.snips = mastersnipper(self, self.events,
                                   bins=int(self.bins),
                                   preTrial=int(self.baseline.get()),
                                   trialLength=int(self.length.get()),
                                   threshold=int(self.noiseth.get()))
        self.noiseindex = self.snips['noise']
        #self.getnoiseindex()

        self.snips_to_plot = self.snips[self.snipsVar.get()]
        
        # plot data
        self.singletrialviewer()
        self.heatmapviewer()
        self.averagesnipsviewer()
        
    def setevents(self):
        try:
            if 'runs' in self.eventsVar.get():
                key=self.eventsVar.get().split('-')
                self.events = self.runs[key[1]]
            else:
                self.eventepoc = getattr(self.epocs, self.eventsVar.get())
                self.events = getattr(self.eventepoc, self.onsetVar.get())
        except:
            alert('Cannot set events')
            
    def setlicks(self):
        try:
            self.lickepoc = getattr(self.epocs, self.lickrunsVar.get())
            self.licks = getattr(self.lickepoc, self.onsetVar.get())
        except:
            alert('Cannot set licks')
  
    def togglenoise(self):
        if self.noise:
            self.noise = False
            self.noiseBtn.config(text="Turn noise on")
        else:
            self.noise = True
            self.noiseBtn.config(text="Turn noise off")
            
        try:
            self.makesnips()
        except: pass
        
    def prevtrial(self):
        print('Selecting prev trial')
        
    def nexttrial(self):
        print('Selecting next trial')
        
    def showall(self):
        print('Showing all trials')

    def makelickruns(self):
        self.setlicks()
        self.runs={}
        self.runs[self.lickrunsVar.get()] = [val for i, val in enumerate(self.licks) if (val - self.licks[i-1] > 10)]
        self.epochfields.append('runs-' + self.lickrunsVar.get())
        self.updateeventoptions()

    def singletrialviewer(self):
        f = Figure(figsize=(2.67,2.67)) # 5,3
        ax = f.add_subplot(111)
        
        if self.noise:
            trialsFig(ax, self.snips_to_plot, pps=self.pps, noiseindex=self.noiseindex)
        else:
            snips = np.asarray([i for (i,v) in zip(self.snips_to_plot, self.noiseindex) if not v])
            trialsFig(ax, snips)
     
        canvas = FigureCanvasTkAgg(f, self.f4)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))
        
    def heatmapviewer(self):
        f = Figure(figsize=(2.67,2.67))
        ax = f.add_subplot(111)
        
        if self.noise:
            snips=self.snips_to_plot
        else:
            snips=np.asarray([i for (i,v) in zip(self.snips_to_plot, self.noiseindex) if not v])
        
        makeheatmap(ax, snips)
        
        canvas = FigureCanvasTkAgg(f, self.f5)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))
        
    def averagesnipsviewer(self):
        
        f = Figure(figsize=(2.67,2.67)) # 5.3
        ax = f.add_subplot(111)
        
        if self.noise:
            snips=self.snips_to_plot
        else:
            snips=np.asarray([i for (i,v) in zip(self.snips_to_plot, self.noiseindex) if not v])

        trialsShadedFig(ax, snips,
                          self.pps,
                          eventText = self.eventsVar.get())
        
        canvas = FigureCanvasTkAgg(f, self.f6)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N,S,E,W))

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
                  threshold=10):
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
        output['filt_z'] = filtTrials_z
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

def trialsFig(ax, trials, pps=1, preTrial=10, scale=5, noiseindex = [],
              plotnoise=True,
              eventText='event', 
              ylabel=''):

    if len(noiseindex) > 0:
        trialsNoise = np.array([i for (i,v) in zip(trials, noiseindex) if v])
        trials = np.array([i for (i,v) in zip(trials, noiseindex) if not v])
        if plotnoise == True:
            ax.plot(trialsNoise.transpose(), c='red', alpha=0.1)
        
    ax.plot(trials.transpose(), c='grey', alpha=0.4)
    ax.plot(np.mean(trials,axis=0), c='k', linewidth=2)
     
    ax.set(ylabel = ylabel)
    ax.xaxis.set_visible(False)
            
    scalebar = scale * pps

    yrange = ax.get_ylim()[1] - ax.get_ylim()[0]
    scalebary = (yrange / 10) + ax.get_ylim()[0]
    scalebarx = [ax.get_xlim()[1] - scalebar, ax.get_xlim()[1]]
    
    ax.plot(scalebarx, [scalebary, scalebary], c='k', linewidth=2)
    ax.text((scalebarx[0] + (scalebar/2)), scalebary-(yrange/50), str(scale) +' s', ha='center',va='top')
 
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    xevent = pps * preTrial  
    ax.plot([xevent, xevent],[ax.get_ylim()[0], ax.get_ylim()[1] - yrange/20],'--')
    ax.text(xevent, ax.get_ylim()[1], eventText, ha='center',va='bottom')
    
    return ax

def trialsShadedFig(ax, trials, pps=1, scale=5, preTrial=10,
                    noiseindex=[],
                    eventText = 'event', ylabel = '',
                    linecolor='k', errorcolor='grey'):
    
    if len(noiseindex) > 0:
        trials = np.array([i for (i,v) in zip(trials, noiseindex) if not v])
    
    trials=np.asarray(trials)
    
    yerror = [np.std(i)/np.sqrt(len(i)) for i in trials.T]
    y = np.mean(trials,axis=0)
    x = np.arange(0,len(y))
    
    ax.plot(x, y, c=linecolor, linewidth=2)

    errorpatch = ax.fill_between(x, y-yerror, y+yerror, color=errorcolor, alpha=0.4)
    
    ax.set(ylabel = ylabel)
    ax.xaxis.set_visible(False)
            
    scalebar = scale * pps

    yrange = ax.get_ylim()[1] - ax.get_ylim()[0]
    scalebary = (yrange / 10) + ax.get_ylim()[0]
    scalebarx = [ax.get_xlim()[1] - scalebar, ax.get_xlim()[1]]
    
    ax.plot(scalebarx, [scalebary, scalebary], c='k', linewidth=2)
    ax.text((scalebarx[0] + (scalebar/2)), scalebary-(yrange/50), '5 s', ha='center',va='top')
 
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    xevent = pps * preTrial
    ax.plot([xevent, xevent],[ax.get_ylim()[0], ax.get_ylim()[1] - yrange/20],'--')
    ax.text(xevent, ax.get_ylim()[1], eventText, ha='center',va='bottom')
    
    return ax

def makeheatmap(ax, data, events=None, ylabel='Trials'):
    ntrials = np.shape(data)[0]
    xvals = np.linspace(-9.9,20,300)
    yvals = np.arange(1, ntrials+2)
    xx, yy = np.meshgrid(xvals, yvals)
    
    mesh = ax.pcolormesh(xx, yy, data, cmap='jet', shading = 'flat')
    
    if events:
        ax.vlines(events, yvals[:-1], yvals[1:], color='w')
    else:
        print('No events')
        
    ax.set_ylabel(ylabel)
    ax.set_yticks([1, ntrials])
    ax.set_xticks([])
    ax.invert_yaxis()
    
    return ax, mesh

root = Tk()

currdir = os.getcwd()
currdir = 'C:\\Users\\jaimeHP\\Documents\\Test Data\\'

app = Window(root)
root.lift()
root.mainloop()

#alltrialVar = StringVar(self.f4)
#ttk.Radiobutton(self.f4, text='All Trials', variable=alltrialVar, value='all').grid(
#        row=0, column=1)
#ttk.Radiobutton(self.f4, text='Single Trial', variable=alltrialVar, value='single').grid(
#        row=1, column=1)
#
#currenttrialVar = IntVar(self.f4)
#currenttrialVar.set(0)
#self.trialEntry = ttk.Entry(self.f4, textvariable=currenttrialVar).grid(
#        row=1, column=2)


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
#
#    def getnoiseindex(self):
#        self.noisemethod = 'sum'
#        self.threshold = 8
#        bgMAD = findnoise(self.data, self.randomevents,
#                              t2sMap = self.t2sMap, fs = self.fs, bins=self.bins,
#                              method=self.noisemethod)          
#        sigSum = [np.sum(abs(i)) for i in self.snips['blue']]
#        sigSD = [np.std(i) for i in self.snips['blue']]
#        self.noiseindex = [i > bgMAD*self.threshold for i in sigSum]