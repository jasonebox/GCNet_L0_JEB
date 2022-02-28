#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 15:50:33 2022

@author: jason

"""

import datetime
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from numpy.polynomial.polynomial import polyfit
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.pyplot import figure
import matplotlib
# -------------------------------- chdir
if os.getlogin() == 'Maiken':
    base_path = '/Users/Maiken/OneDrive/PUK/GCNet_SWVF/'
    z_path='/Users/Maiken/OneDrive/PUK/GCNet_photogrammetry/output/'
elif os.getlogin() == 'jason':
    base_path = '/Users/jason/Dropbox/GCNet_L0_JEB/'

os.chdir(base_path)

font_size=22
th=1
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['grid.color'] = "grey"
plt.rcParams["font.size"] = font_size


df=pd.read_csv(base_path+'/L0_modified/DY2_all_years_L0_modified.csv')
df = df.set_index('time')

df.columns

df['decimal_time']=df.year+df.JulianDay/366.

# plt.plot(df["WindSpeed1"])
# plt.gcf().autofmt_xdate()

#%%

n_rows=2
fig, ax = plt.subplots(n_rows,1,figsize=(10,18))

# from datetime import datetime
plt.close()

t0=datetime(1996, 5, 25,21) ; t1=datetime(1997, 8, 24)

# ax[cc].plot(df.WindSpeed1[t0:t1])

cc=0
for i,sensor_level in enumerate([1,2]):
    print(i)
    # plt.plot(df["SnowHeight"+str(sensor_level+1)][t0:t1])
    plt.plot(df.decimal_time,df["SnowHeight"+str(sensor_level)])

# ax.set_xlim(t0,t1)
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=1000))   #to get a tick every 15 minutes
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
# xcolor='darkblue'
# ax.xaxis.label.set_color(xcolor)
# ax.tick_params(axis='x', colors=xcolor)
mult=0.8
# ax.text(-0.15,0.0, "day of\nAug.'21",transform=ax.transAxes, fontsize=font_size*mult,
#     verticalalignment='top',rotation=0,color=xcolor, rotation_mode="anchor")  

# ticks = ax.get_xticks()
# labels = ax.get_xticklabels()
# n = len(ticks) // 10  # Show 10 ticks.
# ax.set_xticks(ticks[::n])
# ax.set_xticklabels(labels[::n])

# plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center' )

# ax[cc].set_xlim(t0,t1)
# ax[cc].xaxis.set_major_locator(mdates.DayLocator(interval=100)) 
# ax[cc].xaxis.set_major_formatter(mdates.DateFormatter('%d'))
# xcolor='darkblue'
# ax[cc].xaxis.label.set_color(xcolor)
# ax[cc].tick_params(axis='x', colors=xcolor)
# mult=0.8
# ax[cc].text(-0.15,0.0, "day of\nAug.'21",transform=ax[cc].transAxes, fontsize=font_size*mult,
#     verticalalignment='top',rotation=0,color=xcolor, rotation_mode="anchor")  
# plt.setp(ax[cc].xaxis.get_majorticklabels(), rotation=90,ha='center' )

plt.show()
# dates=['1996-05-25',
#        '1996-06-25']
# min_z=['0.01',
#        '0.2']