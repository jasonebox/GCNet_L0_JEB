#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 15:50:33 2022

@author: jason

if (stnum(jx) eq '08') then begin
  adjust_z,d2,nlines,17,17,1998,118.8750,0.95
  adjust_z,d2,nlines,18,18,1998,118.8750,2.25
  adjust_z,d2,nlines,17,17,1999,1.,0.95
  adjust_z,d2,nlines,18,18,1999,1.,2.25
  adjust_z,d2,nlines,17,17,2000,1.,1.022
  adjust_z,d2,nlines,18,18,2000,1.,2.1993
  adjust_z,d2,nlines,icol,fcol,2000,134.,2.4
  adjust_z,d2,nlines,icol,fcol,2003,129.8333,2.3
endif

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

fn='./ancil/varnames.txt'
df_names=pd.read_csv(fn,names=['ID','varnam'],delim_whitespace=True)

#%% read N *a.dat files
from glob import glob

files = sorted(glob("./L0_raw/08_*.dat"), reverse=False)

#%%
i=0
dfx=pd.read_csv(files[i],names=df_names.varnam,delim_whitespace=True)
dfx['date']=pd.to_datetime(dfx['JulianDay'], format='%j').dt.strftime('%Y-%m-%d %H')
dfx['date'] = pd.to_datetime(dfx.date) + pd.offsets.DateOffset(years=dfx.year[0]-1900)

pdList = []

# for i,file in enumerate(files):
for i,file in enumerate(files[0:4]):
    dfx=pd.read_csv(files[i],names=df_names.varnam,delim_whitespace=True)
    dfx[dfx<-990]=np.nan
    dfx[dfx==999]=np.nan

    dfx['date']=pd.to_datetime(dfx['JulianDay'], format='%j').dt.strftime('%Y-%m-%d-%H')
    dfx['hour']=(dfx['JulianDay']-dfx['JulianDay'].astype(int))*24
    dfx.hour=dfx.hour.round(0).astype(int)
    # print(dfx.hour)
    # #%%
    dfx['date'] = pd.to_datetime(dfx.date) + pd.offsets.DateOffset(years=dfx.year[0]-1900)
    print(i,file,dfx.year[0]-1900)

    pdList.append(dfx)
    print(dfx)
df = pd.concat(pdList)

print(df)
df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month
df['day'] = pd.DatetimeIndex(df['date']).day
# df['hour'] = pd.DatetimeIndex(df['date']).hour

df['time']=pd.to_datetime(df[['year', 'month', 'day', 'hour']])

df = df.set_index('time')

#%% form a more continuous air temperature record by gap-filling TC air T with the thermister air T

for sensor_level in range(1,3):
    print(sensor_level)
    df['AirTemp'+str(sensor_level)]=df['AirTemp'+str(sensor_level)+'(TC)']
    print(sum(~np.isfinite(df['AirTemp'+str(sensor_level)])))
    v=((~np.isfinite(df['AirTemp'+str(sensor_level)]))& (np.isfinite(df['AirTemp'+str(sensor_level)+'(CS500)'])))
    print(sum(v))
    df['AirTemp'+str(sensor_level)][v]=1.#df['AirTemp'+str(sensor_level)+'(CS500)'][v]
    print(sum(~np.isfinite(df['AirTemp'+str(sensor_level)])))

#%% apply speed of sound correction to sonic height sensor data
for sensor_level in range(1,3):
    print(sensor_level)
    Tk=df['AirTemp'+str(sensor_level)].astype(float)+273.15
    Tr=(Tk/273.15)**0.5
    df["SnowHeight"+str(sensor_level)]*=Tr

#%% clean check initial snow height data


df["SnowHeight1"][0:50][df["SnowHeight1"][0:50]<2.5]=np.nan
df["SnowHeight1"][0:50][df["SnowHeight1"][0:50]>2.85]=np.nan
df["SnowHeight2"][0:50][df["SnowHeight2"][0:50]<3.1]=np.nan
df["SnowHeight2"][0:50][df["SnowHeight2"][0:50]>3.3]=np.nan

plt.plot(df["SnowHeight1"][0:50])
plt.plot(df["SnowHeight2"][0:50])

#%% initialise zero value for height using valid cases from the start of the record
site='DY2'
if site=='DY2':
    # exclude spurious outliers
    z1=np.nanmean(df["SnowHeight1"][0:50])
    z2=np.nanmean(df["SnowHeight2"][0:50])

print(z1,z2)


#%%
df.SnowHeight1=z1-df.SnowHeight1
df.SnowHeight2=z2-df.SnowHeight2


#%% filer impossible height values

# df.SnowHeight1[df.SnowHeight1>8]=np.nan
# df.SnowHeight1[df.SnowHeight1<0.2]=np.nan

for i,sensor_level in enumerate(range(1,3)):
    print(sensor_level)
    df["SnowHeight"+str(sensor_level)][df["SnowHeight"+str(sensor_level)]<-1]=np.nan
    df["SnowHeight"+str(sensor_level)][df["SnowHeight"+str(sensor_level)]>9]=np.nan
    
plt.plot(z1-df.SnowHeight1)
plt.plot(z2-df.SnowHeight2)

# t0=datetime(df.year[v[0][0]], df.month[v[0][0]],df.day[v[0][0]]-1,df.hour[v[0][0]])
# t1=datetime(df.year[v[0][0]], df.month[v[0][0]],df.day[v[0][0]],df.hour[v[0][0]])

# dz=df.SnowHeight1[t1]-df.SnowHeight1[t0]
# print(dz)

# df.SnowHeight1[t1:]-=dz

# df.columns

# if (stnum(jx) eq '08') then begin
#   sm_lim_filter,nlines,d2,18,18,varname,mod_count,2.4,2.7,333.2917,366.9583,year,1996.

#   sm_lim_filter,nlines,d2,17,17,varname,mod_count,1,1.3,34,60,year,1998
#   sm_lim_filter,nlines,d2,17,17,varname,mod_count,0.8,1.2,105,128,year,1998
#   sm_lim_filter,nlines,d2,18,18,varname,mod_count,1.,1.6,105,128,year,1998

#   sm_lim_filter,nlines,d2,18,18,varname,mod_count,0.5,1.6,197,238.5,year,1999

#   sm_lim_filter,nlines,d2,17,17,varname,mod_count,-0.122,1,1,13,year,2000
#   sm_lim_filter,nlines,d2,17,17,varname,mod_count,-0.9,1,1,275,year,2000
#   sm_lim_filter,nlines,d2,17,17,varname,mod_count,-1.3,1,275,367,year,2000
#   sm_lim_filter,nlines,d2,fcol,fcol,varname,mod_count,-0.2,1,1,256,year,2000
#   sm_lim_filter,nlines,d2,fcol,fcol,varname,mod_count,-0.9,1,256,367,year,2000

#   sm_lim_filter,nlines,d2,icol,icol,varname,mod_count,1.6,5,1,157,year,2001
#   sm_lim_filter,nlines,d2,fcol,fcol,varname,mod_count,3.1,5,1,157,year,2001

#   sm_lim_filter,nlines,d2,icol,fcol,varname,mod_count,-999,-99,140.7083,367,year,2002
#   sm_lim_filter,nlines,d2,fcol,fcol,varname,mod_count,2.43,2.7,1,140.7083,year,2002
#   last_val,nlines,d2,icol,fcol,varname,mod_count,modvar

#   sm_lim_filter,nlines,d2,icol,icol,varname,mod_count,1,5,1,360,year,2003

# endif
# plt.plot(df.SnowHeight1)
# t0=datetime(1998,4,25,20)
# t1=datetime(1998,4,30,1)
# plt.plot(df.SnowHeight1[t0:t1],'-o')
# plt.plot(df.SnowHeight2[t0:t1],'-o')



#%% adjust height data for station changes by people


N=len(df)

adjustment_year=[1998,2000]
adjustment_decimal_day_of_year=[118.8750,134.]
adjustment_dz=[[0.95,2.4],[2.25,2.25]]

for j in range(len(adjustment_decimal_day_of_year)):
    for i,sensor_level in enumerate(range(1,3)):
        print(j,i,sensor_level)
        v=np.where(((df.year==adjustment_year[j])&(df.JulianDay==adjustment_decimal_day_of_year[j])))
        if len(v[0]):
            v=v[0][0]
            print(v,adjustment_dz[i][j])
            df["SnowHeight"+str(sensor_level)][v:N]+=adjustment_dz[i][j]
        
#%%
plt.close()

for i,sensor_level in enumerate(range(1,3)):
    plt.plot(df["SnowHeight"+str(sensor_level)],'.')

#%% copy to another dataframe to avoid needing to rerun the above
aws=df

##%%


##%% read observed instrument height data

obs_df = pd.read_excel('/Users/jason/Dropbox/GCNet_SWVF/ancil/GCNet_maintenance.xlsx',sheet_name="DYE-2",engine='openpyxl')
# print(obs_df)

obs_df["Date"]=pd.to_datetime(obs_df['Date (dd-mm-yyyy HH:MM)'])
#obs_df.index = pd.to_datetime(obs_df.time)


plt.close()

n_rows=2
fig, ax = plt.subplots(n_rows,1,figsize=(16,10))

case_id=0
print('profile instrument separation before dz',obs_df['W2 after (cm)'][case_id]-obs_df['W1 after (cm)'][case_id])
print('profile instrument separation after dz',obs_df['W2 after (cm)'][case_id]-obs_df['W1 after (cm)'][case_id])
profile_dz=(obs_df['W2 after (cm)'][case_id]-obs_df['W1 after (cm)'][case_id])/100

for i,sensor_level in enumerate(range(1,3)):
    aws['THW_z'+str(sensor_level)]=obs_df['W'+str(sensor_level)+' before (cm)'][0]/100-aws["SnowHeight"+str(sensor_level)]
    if i:aws['THW_z'+str(sensor_level)]+=profile_dz
    cc=0
    ax[cc].plot(df["SnowHeight"+str(sensor_level)],'.',label='snow height '+str(sensor_level))
    ax[cc].set_ylabel('surface height, m', color='k')
    ax[cc].set_xticklabels([])
    ax[cc].legend()
    cc=1
    ax[cc].plot(aws['THW_z'+str(sensor_level)],'.',label='instrument height '+str(sensor_level))
    ax[cc].set_ylabel('instrument height, m', color='k')
    mult=1
    ax[cc].legend(prop={'size': font_size*mult})
    # ax[cc].set_ylim(np.nanmin(y),np.nanmax(y))     
    ax[cc].get_xaxis().set_visible(True)
    ax[cc].legend(prop={'size': font_size})
    ax[cc].legend()
    # ax[cc].set_xlim(t0,t1)

plt.setp(ax[1].xaxis.get_majorticklabels(), rotation=90,ha='center' )
fig.tight_layout(pad=1.0)
plt.show()
#%% adjust for mast extensions and profile level adjustments

from datetime import datetime

# x=obs_df["Date"][1].strftime('%d-%m-%y')
# x=pd.Timestamp(obs_df["Date"][1])

case_id=4 # 1998 visit, noted in field notes, tower extension AND change in profile separation
print("case",obs_df["Date"][case_id].strftime('%d-%m-%y'))
print("wind z 1 before",obs_df['W1 before (cm)'][case_id]/100)
print("wind z 1 after",obs_df['W1 after (cm)'][case_id]/100)
print('profile instrument separation dz',obs_df['W2 after (cm)'][case_id]-obs_df['W1 after (cm)'][case_id])

tx=obs_df["Date"][case_id].to_pydatetime().date()
dz=np.zeros(2)
for i,sensor_level in enumerate(range(1,3)):
    dz[i]=np.nanmean(obs_df['W'+str(sensor_level)+' after (cm)'][case_id]/100-aws['THW_z'+str(sensor_level)][aws.date.dt.date==tx])
    print('dz',1,dz[i])


plt.close()

n_rows=2
fig, ax = plt.subplots(n_rows,1,figsize=(16,10))

for i,sensor_level in enumerate(range(1,3)):
    aws['THW_z'+str(sensor_level)]=obs_df['W'+str(sensor_level)+' before (cm)'][0]/100-aws["SnowHeight"+str(sensor_level)]
    cc=0
    ax[cc].plot(df["SnowHeight"+str(sensor_level)],'.',label='snow height '+str(sensor_level))
    ax[cc].set_ylabel('snow height, m', color='k')
    ax[cc].set_xticklabels([])
    ax[cc].legend()

    cc=1
    aws['THW_z'+str(sensor_level)][aws.date.dt.date>tx]+=dz[i]
    ax[cc].plot(aws['THW_z'+str(sensor_level)],'.',label='instrument height '+str(sensor_level))
    ax[cc].set_ylabel('instrument height, m', color='k')
    mult=1
    ax[cc].legend(prop={'size': font_size*mult})
    # ax[cc].set_ylim(np.nanmin(y),np.nanmax(y))     
    ax[cc].get_xaxis().set_visible(True)
    ax[cc].legend(prop={'size': font_size})
    # ax[cc].set_xlim(t0,t1)
    ax[cc].legend()

plt.setp(ax[1].xaxis.get_majorticklabels(), rotation=90,ha='center' )
fig.tight_layout(pad=1.0)



#%% verify
plt.close()

n_rows=3
fig, ax = plt.subplots(n_rows,1,figsize=(16,14))

case_id=5 # 1999 visit, noted in field notes, no change in instrument heights
tx=obs_df["Date"][case_id].to_pydatetime().date()
print(tx)

for i,sensor_level in enumerate(range(1,3)):
    cc=0
    ax[cc].plot(df["SnowHeight"+str(sensor_level)],'.',label='snow height '+str(sensor_level))
    ax[cc].set_ylabel('snow height, m', color='k')
    ax[cc].set_xticklabels([])
    ax[cc].legend()

    cc=1
    ax[cc].plot(aws['THW_z'+str(sensor_level)],'.',label='instrument height '+str(sensor_level))
    ax[cc].set_ylabel('instrument height, m', color='k')
    mult=1
    ax[cc].legend(prop={'size': font_size*mult})
    # ax[cc].set_ylim(np.nanmin(y),np.nanmax(y))     
    ax[cc].legend(prop={'size': font_size})
    ax[cc].set_xticklabels([])
    # ax[cc].set_xlim(t0,t1)
    ax[cc].legend()

    t1=obs_df['W'+str(sensor_level)+' before (cm)'][case_id]
    t2=aws['THW_z'+str(sensor_level)][aws.date.dt.date==tx][0]
    ax[cc].text(tx,aws['THW_z'+str(sensor_level)][aws.date.dt.date==tx][0],"{:.2f}".format(t1)+'\n'+"{:.2f}".format(t2),rotation=45)
    ax[cc].text(tx,0,str(tx),rotation=0)

cc=2
ax[cc].set_ylabel('profile separation, m', color='k')
ax[cc].plot(aws['THW_z'+str(2)]-aws['THW_z'+str(1)],'.',label='dz')
ax[cc].legend()
ax[cc].get_xaxis().set_visible(True)

plt.setp(ax[1].xaxis.get_majorticklabels(), rotation=90,ha='center' )
fig.tight_layout(pad=1.0)
#%% write out dataframe
# aws.to_csv(base_path+'/L0_modified/DY2_all_years_L0_modified.csv')
