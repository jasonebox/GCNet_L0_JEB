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

#%%

plt.close()

for i,sensor_level in enumerate(range(1,3)):
    plt.plot(df["SnowHeight"+str(sensor_level)],'.')

dates=['1996-05-25',
       '1996-06-25']
min_z=['0.01',
       '0.2']