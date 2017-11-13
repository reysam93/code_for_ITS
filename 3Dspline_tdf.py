#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 05:00:11 2017

@author: antoniocaamano
"""

from numpy import arange, cos, linspace, pi, sin, random
from scipy.interpolate import splprep, splev
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Where to save the figures
PROJECT_ROOT_DIR = "/Users/antoniocaamano/Documents/investigacion/collision/"
PART_ID = "traffic_cluster"

def save_fig(fig_id, tight_layout=True):
    path = os.path.join(PROJECT_ROOT_DIR, "images", PART_ID, fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)



plt.rcParams['text.usetex'] = False
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


df = pd.read_csv('/Users/antoniocaamano/Documents/investigacion/collision/data/trash_tests/3Dcurve3.csv')
x=df.x
y=df.y
z=df.z


# spline parameters
s=1.0 # smoothness parameter
k=3 # spline order
nest=100 # estimate of number of knots needed (-1 = maximal)

# find the knot points
tckp,u = splprep([x,y,z],s=s,k=k,nest=nest)

# evaluate spline, including interpolated points
xnew,ynew,znew = splev(linspace(0,1,10000),tckp)

import pylab
pylab.subplot(2,2,1)
data,=pylab.plot(z,y,'bo-',label='data')
fit,=pylab.plot(znew,ynew,'r-',label='fit')
pylab.legend()
pylab.xlabel('Density')
pylab.ylabel('Flow')

pylab.subplot(2,2,2)
data,=pylab.plot(x,y,'bo-',label='data')
fit,=pylab.plot(xnew,ynew,'r-',label='fit')
pylab.legend()
pylab.ylabel('Flow')
pylab.xlabel('time')

pylab.subplot(2,2,3)
data,=pylab.plot(x,z,'bo-',label='data')
fit,=pylab.plot(xnew,znew,'r-',label='fit')
pylab.legend()
pylab.ylabel('Density')
pylab.xlabel('time')


pylab.savefig('splprep_demo.png')



#3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter( y, z, x, c='blue', marker='o')
ax.scatter( ynew, znew, xnew, c='red', marker='.')
ax.set_xlabel('Flow')
ax.set_ylabel('Density')
ax.set_zlabel('time')
#ax.view_init(0, -45)
plt.tight_layout()
#plt.show()
plt.savefig('3dinterp.png', format='png', dpi=300)