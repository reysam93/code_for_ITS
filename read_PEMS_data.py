#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 14:08:41 2017

@author: antoniocaamano
"""

#Script to incorporate de PEMS DOT Data to account for shear traffic among lanes and look for relation to accidents
#Test script to look for shear patterns in a month in the 

# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

# Common imports
import glob
import numpy as np
import numpy.random as rnd
import os
import pandas as pd
from pandas.tseries import converter as pdtc
from pandas.tseries.offsets import *


# to make this code's output stable across runs
rnd.seed(42)

# To plot pretty figures

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime



plt.rcParams['text.usetex'] = False
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
#plt.rcParams['ax.tick_params'] = 'in'

import matplotlib.dates as md
#proper times in figures

# Where to save the figures
PROJECT_ROOT_DIR = "/Users/antoniocaamano/Documents/investigacion/collision/"
PART_ID = "traffic_cluster"

def save_fig(fig_id, tight_layout=True):
    path = os.path.join(PROJECT_ROOT_DIR, "images", PART_ID, fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)

COLLISION_PATH = os.path.join(PROJECT_ROOT_DIR , "data/PEMS/N. Aquatic Park_downstream_PM_5.25/occ/December/")
    
def load_collision_data(collision_path=COLLISION_PATH):
#    csv_path = os.path.join(collision_path, "pems.dot.ca.gov1.txt")
    return pd.read_table(csv_path,sep='\t', index_col=None, na_values=['NA'])




    
if __name__ == "__main__":
     print("Loading New Road dataset")
     
     
#     traffic=load_collision_data()
     
     path =COLLISION_PATH 
     allFiles = glob.glob(path + "/*.txt")
     traffic = pd.DataFrame()
     list_ = []
     for file_ in allFiles:
         traffic = pd.read_table(file_,sep='\t', index_col=None, na_values=['NA'],header=0)
         list_.append(traffic)
         traffic = pd.concat(list_)
     
     
     traffic.columns=['date','flow_lane_1','speed_lane_1','flow_lane_2','speed_lane_2','flow_lane_3','speed_lane_3','flow_lane_4','speed_lane_4','flow_lane_5','speed_lane_5','agg_flow','agg_speed','lane_points','obs']
     traffic.index=pd.to_datetime(traffic.date)
    
     traffic['dens_1']=np.true_divide(traffic.flow_lane_1*12,traffic.speed_lane_1)
     traffic['dens_2']=np.true_divide(traffic.flow_lane_2*12,traffic.speed_lane_2)
     traffic['dens_3']=np.true_divide(traffic.flow_lane_3*12,traffic.speed_lane_3)
     traffic['dens_4']=np.true_divide(traffic.flow_lane_4*12,traffic.speed_lane_4)
     traffic['dens_5']=np.true_divide(traffic.flow_lane_5*12,traffic.speed_lane_5)

#     traffic['dens_1']=np.true_divide(12,traffic.speed_lane_1)
#     traffic['dens_2']=np.true_divide(12,traffic.speed_lane_2)
#     traffic['dens_3']=np.true_divide(12,traffic.speed_lane_3)
#     traffic['dens_4']=np.true_divide(12,traffic.speed_lane_4)
#     traffic['dens_5']=np.true_divide(12,traffic.speed_lane_5)
#    
   
     traffic['grad_dens_12']=np.subtract(traffic.dens_1,traffic.dens_2)
     traffic['grad_dens_23']=np.subtract(traffic.dens_2,traffic.dens_3)
     traffic['grad_dens_34']=np.subtract(traffic.dens_3,traffic.dens_4)
     traffic['grad_dens_45']=np.subtract(traffic.dens_4,traffic.dens_5)
     
     traffic['grad_flow_12']=np.subtract(traffic.flow_lane_1,traffic.flow_lane_2)
     traffic['grad_flow_23']=np.subtract(traffic.flow_lane_2,traffic.flow_lane_3)
     traffic['grad_flow_34']=np.subtract(traffic.flow_lane_3,traffic.flow_lane_4)
     traffic['grad_flow_45']=np.subtract(traffic.flow_lane_4,traffic.flow_lane_5)
     
     
 
#     traffic.loc[:,'traffic.grad_dens_12':'traffic.grad_dens_45']].plot()

     grad_density_f=traffic.loc[:,'grad_dens_12':'grad_dens_45']
    
    
     grad_density_f['Day'] = map(lambda x: x.day, grad_density_f.index)
     weekdays_only=grad_density_f[grad_density_f.index.dayofweek<5] 
     weekends_only=grad_density_f[grad_density_f.index.dayofweek>4] 
    
    
     grad_flow_f=traffic.loc[:,'grad_flow_12':'grad_flow_45']
    
    
     grad_flow_f['Day'] = map(lambda x: x.day, grad_flow_f.index)
     weekdays_only_f=grad_flow_f[grad_flow_f.index.dayofweek<5] 
     weekends_only_f=grad_flow_f[grad_flow_f.index.dayofweek>4] 
    
#   Plotting the inter-lane density fluctuations
#     fig, ax = plt.subplots(1,1)
#     traffic.grad_dens_12.plot(ax=ax)
#     fig, ax = plt.subplots(1,1)
#     traffic.grad_dens_23.plot(ax=ax)
#     fig, ax = plt.subplots(1,1)
#     traffic.grad_dens_34.plot(ax=ax)
#     fig, ax = plt.subplots(1,1)
#     traffic.grad_dens_45.plot(ax=ax)
#     save_fig('NAquaticPark_downstream_PM_525_1week')

#   Plotting the lane flow fluctuations  
#     fig, ax = plt.subplots(1,1)
#     traffic.grad_flow_12.plot(ax=ax)
#     fig, ax = plt.subplots(1,1)
#     traffic.grad_flow_23.plot(ax=ax)
#     fig, ax = plt.subplots(1,1)
#     traffic.grad_flow_34.plot(ax=ax)
#     fig, ax = plt.subplots(1,1)
#     traffic.grad_flow_45.plot(ax=ax)


#Inter-Lane density fluctuations daily
     fig, ax = plt.subplots(1,1)
     weekdays_only.groupby('Day').plot(x=grad_density_f.index.time[0:288], y='grad_dens_12',ax=ax,legend=False,alpha=0.5,rot=45)
     save_fig('N_AquaticPark_downstream_PM_525_weekdays_grad_dens_12_speed_Dec')
#     fig, ax = plt.subplots(1,1)
#     weekends_only.groupby('Day').plot(x=grad_density_f.index.time[0:288], y='grad_dens_12',ax=ax,legend=False,alpha=0.5,rot=45)
#     save_fig('N_AquaticPark_downstream_PM_525_weekends_grad_dens_12_speed_Dec')
#     
     fig, ax = plt.subplots(1,1)
     weekdays_only.groupby('Day').plot(x=grad_density_f.index.time[0:288], y='grad_dens_23',ax=ax,legend=False,alpha=0.5,rot=45)
     save_fig('N_AquaticPark_downstream_PM_525_weekdays_grad_dens_23_speed_Dec')
#     fig, ax = plt.subplots(1,1)
#     weekends_only.groupby('Day').plot(x=grad_density_f.index.time[0:288], y='grad_dens_23',ax=ax,legend=False,alpha=0.5,rot=45)
#     save_fig('N_AquaticPark_downstream_PM_525_weekends_grad_dens_23_speed_Dec')
     
     fig, ax = plt.subplots(1,1)
     weekdays_only.groupby('Day').plot(x=grad_density_f.index.time[0:288], y='grad_dens_34',ax=ax,legend=False,alpha=0.5,rot=45)
     save_fig('N_AquaticPark_downstream_PM_525_weekdays_grad_dens_34_speed_Dec')
#     fig, ax = plt.subplots(1,1)
#     weekends_only.groupby('Day').plot(x=grad_density_f.index.time[0:288], y='grad_dens_34',ax=ax,legend=False,alpha=0.5,rot=45)
#     save_fig('N_AquaticPark_downstream_PM_525_weekends_grad_dens_34_speed_Dec')
#     
     fig, ax = plt.subplots(1,1)
     weekdays_only.groupby('Day').plot(x=grad_density_f.index.time[0:288], y='grad_dens_34',ax=ax,legend=False,alpha=0.5,rot=45)
     save_fig('N_AquaticPark_downstream_PM_525_weekdays_grad_dens_45_speed_Dec')
#     fig, ax = plt.subplots(1,1)
#     weekends_only.groupby('Day').plot(x=grad_density_f.index.time[0:288], y='grad_dens_34',ax=ax,legend=False,alpha=0.5,rot=45)
#     save_fig('N_AquaticPark_downstream_PM_525_weekends_grad_dens_45_speed_Dec')

#Inter-Lane flow fluctuations daily


     fig, ax = plt.subplots(1,1)
     weekdays_only_f.groupby('Day').plot(x=grad_flow_f.index.time[0:288], y='grad_flow_12',ax=ax,legend=False,alpha=0.5,rot=45)
     save_fig('N_AquaticPark_downstream_PM_525_weekdays_grad_flow_12_speed_Dec')
#     fig, ax = plt.subplots(1,1)
#     weekends_only_f.groupby('Day').plot(x=grad_flow_f.index.time[0:288], y='grad_flow_12',ax=ax,legend=False,alpha=0.5,rot=45)
#     save_fig('N_AquaticPark_downstream_PM_525_weekends_grad_flow_12_speed_Dec')
#     
     fig, ax = plt.subplots(1,1)
     weekdays_only_f.groupby('Day').plot(x=grad_flow_f.index.time[0:288], y='grad_flow_23',ax=ax,legend=False,alpha=0.5,rot=45)
     save_fig('N_AquaticPark_downstream_PM_525_weekdays_grad_flow_23_speed_Dec')
#     fig, ax = plt.subplots(1,1)
#     weekends_only_f.groupby('Day').plot(x=grad_flow_f.index.time[0:288], y='grad_flow_23',ax=ax,legend=False,alpha=0.5,rot=45)
#     save_fig('N_AquaticPark_downstream_PM_525_weekends_grad_flow_23_speed_Dec')
#     
     fig, ax = plt.subplots(1,1)
     weekdays_only_f.groupby('Day').plot(x=grad_flow_f.index.time[0:288], y='grad_flow_34',ax=ax,legend=False,alpha=0.5,rot=45)
     save_fig('N_AquaticPark_downstream_PM_525_weekdays_grad_flow_34_speed_Dec')
#     fig, ax = plt.subplots(1,1)
#     weekends_only_f.groupby('Day').plot(x=grad_flow_f.index.time[0:288], y='grad_flow_34',ax=ax,legend=False,alpha=0.5,rot=45)
#     save_fig('N_AquaticPark_downstream_PM_525_weekends_grad_flow_34_speed_Dec')
#     
     fig, ax = plt.subplots(1,1)
     weekdays_only_f.groupby('Day').plot(x=grad_flow_f.index.time[0:288], y='grad_flow_34',ax=ax,legend=False,alpha=0.5,rot=45)
     save_fig('N_AquaticPark_downstream_PM_525_weekdays_grad_flow_45_speed_Dec')
#     fig, ax = plt.subplots(1,1)
#     weekends_only_f.groupby('Day').plot(x=grad_flow_f.index.time[0:288], y='grad_flow_34',ax=ax,legend=False,alpha=0.5,rot=45)
#     save_fig('N_AquaticPark_downstream_PM_525_weekends_grad_flow_45_speed_Dec')

     traffic.hist('grad_dens_12',bins=30)
     traffic.hist('grad_dens_23',bins=30)
     traffic.hist('grad_dens_34',bins=30)
     traffic.hist('grad_dens_45',bins=30)
    
    
     traffic.hist('grad_flow_12',bins=30)
     traffic.hist('grad_flow_23',bins=30)
     traffic.hist('grad_flow_34',bins=30)
     traffic.hist('grad_flow_45',bins=30)