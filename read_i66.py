s compañero...#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 09:24:36 2017

@author: antoniocaamano
"""


# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

# Common imports
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

COLLISION_PATH = os.path.join(PROJECT_ROOT_DIR , "data/pandata/")
    
def load_collision_data(collision_path=COLLISION_PATH):
    csv_path = os.path.join(collision_path, "I-66Incident.csv")
    return pd.read_table(csv_path,sep=',', index_col=None, na_values=['NA'])
    
if __name__ == "__main__":
    
    print("Loading I66 dataset")
    traffic=load_collision_data()
    
#    Selecting only cars from both lanes
    lane1=traffic.loc[lambda traffic: traffic.Lane == 1, :]
    cars_lane1=lane1.loc[lambda lane1: lane1.VehicleBinNumber == 1, :]
    lane2=traffic.loc[lambda traffic: traffic.Lane == 2, :]
    cars_lane2=lane2.loc[lambda lane2: lane2.VehicleBinNumber == 1, :]
     
    cars_lane1_vel=cars_lane1.loc[:,'<5 MPH':'<80 MPH']
    cars_lane2_vel=cars_lane2.loc[:,'<5 MPH':'<80 MPH']
    
    speed = pd.Series([5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0],index=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
    
#    speed = pd.Series([5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0],index=['<5 MPH','<10 MPH','<15 MPH','<20 MPH','<25 MPH','<30 MPH','<35 MPH','<40 MPH','<45 MPH','<50 MPH','<55 MPH','<60 MPH','<65 MPH','<70 MPH','<75 MPH','<80 MPH'])

    kinda_shear_12=np.subtract(cars_lane1_vel,cars_lane2_vel)


    inv_sp=np.true_divide(1,speed)

    grad_density={'grad_dens_12': np.dot(kinda_shear_12,inv_sp)}
    grad_density_f=pd.DataFrame(grad_density,index=pd.to_datetime(cars_lane1.StartDate))
    grad_density_f.plot()
    save_fig('grad_density_i66_coll')