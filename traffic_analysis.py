# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 09:29:26 2017

@author: samuel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn import metrics
from sklearn.cluster import DBSCAN

from datetime import datetime
import glob


CRASH_PATH = "./ITS_Primero/HSIS_2006_crash_data.xlsx"
OCC_PATH = "./ITS_Primero/N_Aquatic_Park_downstream_PM_5.25/occ/November/pems.dot.ca.gov45.txt"
SPEED_PATH = "./ITS_Primero/N_Aquatic_Park_downstream_PM_5.25/speed/November/pems.dot.ca.gov45_45.txt"
ROOT_OCC_PATH = "./ITS_Primero/N_Aquatic_Park_downstream_PM_5.25/occ/"
ROOT_SPEED_PATH = "./ITS_Primero/N_Aquatic_Park_downstream_PM_5.25/speed/"
ACCIDENT_MONTHS = ["August", "September", "October", "November", "December"]
MAX_PLOTS = 10


def read_accidents(start_date, end_date, severity):
    accidents = pd.read_excel(CRASH_PATH)
    accidents = accidents[(accidents['milepost'] >= 3.89)
                            & (accidents['milepost'] <= 5.25)
                            & (accidents['rte_nbr'] == 80)
                            & (accidents['county'] == 1)
                            & (accidents['severity'] <= severity)]

    dates = accidents.acc_date*10000+accidents.hour
    accidents['acc_date'] = pd.to_datetime(dates, format='%Y%m%d%H%M')
                            
    accidents = accidents[(accidents['acc_date'] >= start_date)
                            & (accidents['acc_date'] <= end_date)]
                            
        
    print(len(accidents.index), "accidents")
    return accidents
    

def read_accident_occ(month):
    files = []
    occ_list = []
    #for month in ACCIDENT_MONTHS:
    files = glob.glob(ROOT_OCC_PATH + month + "/*.txt")
    for file in files:
        occ_list.append(pd.read_table(file))
        
    return pd.concat(occ_list)
   

def read_accident_speed(month):
    files = []
    speed_list = []
    files = glob.glob(ROOT_SPEED_PATH + month + "/*.txt")
    for file in files:
        speed_list.append(pd.read_table(file))
        
    return pd.concat(speed_list)
     

def setLabels(ax, xlabel, ylabel):
    for ax_line in ax:
        for ax_col in ax_line:
            ax_col.set_xlabel(xlabel)
            ax_col.set_ylabel(ylabel)
    

def plotOcc(data, date="", ax=[], marker=None):
    times = [];
    for time in data["5 Minutes"]:
        times.append(datetime.strptime(time, '%m/%d/%Y %H:%M'))
    
    if ax == []:
        fig, ax = plt.subplots(1, 3)

    if date == "":
        title = ""
    else:
        title = date + ": "

    print("Representing the Occupancy")
    ax[0].plot(times, data["Occupancy (%)"], marker=marker)
    ax[0].set_title(title + "Total Occ")
    ax[1].plot(times, data["Lane 1 Occ (%)"], label="line 1", marker=marker)

    ax[1].plot(times, data["Lane 5 Occ (%)"], label="line 5", marker=marker)
    ax[1].set_title(title + "Occ per lane")
    if marker == None:
        ax[1].legend()
    
    ax[2].plot(times, data["Lane 1 Occ (%)"], label="line 1", marker=marker)
    ax[2].plot(times, data["Lane 2 Occ (%)"], label="line 2", marker=marker)
    ax[2].plot(times, data["Lane 3 Occ (%)"], label="line 3", marker=marker)
    ax[2].plot(times, data["Lane 4 Occ (%)"], label="line 4", marker=marker)
    ax[2].plot(times, data["Lane 5 Occ (%)"], label="line 5", marker=marker)
    ax[2].set_title(title + "Occ per lane (all)")
    if marker == None:
        ax[2].legend()
        
    plt.suptitle(title + "Occupancy")
   
        
def plotSpeed(data, date="", ax=[], marker=None):
    times = [];
    for time in data["5 Minutes"]:
        times.append(datetime.strptime(time, '%m/%d/%Y %H:%M'))
        
    if ax == []:
        fig, ax = plt.subplots(1, 3)      
        
    if date == "":
        title = ""
    else:
        title = date + ": "        
        
    print("Representing the Speed")
    ax[0].plot(times, data["Speed (mph)"], marker=marker)
    ax[0].set_title(title + "Total Speed")
    
    ax[1].plot(times, data["Lane 1 Speed (mph)"], label="line 1", marker=marker)
    ax[1].plot(times, data["Lane 5 Speed (mph)"], label="line 5", marker=marker)
    ax[1].set_title(title + "Speed per lane")
    if marker == None:    
        ax[1].legend()

    ax[2].plot(times, data["Lane 1 Speed (mph)"], label="line 1", marker=marker)
    ax[2].plot(times, data["Lane 2 Speed (mph)"], label="line 2", marker=marker)
    ax[2].plot(times, data["Lane 3 Speed (mph)"], label="line 3", marker=marker)
    ax[2].plot(times, data["Lane 4 Speed (mph)"], label="line 4", marker=marker)
    ax[2].plot(times, data["Lane 5 Speed (mph)"], label="line 5", marker=marker)    
    ax[2].set_title(title + "Speed per lane (all)")
    if marker == None:
        ax[2].legend()
        
    plt.suptitle(title + "Speed")
    

def plotSpeedVsOcc(occ, speed):
    times = [];
    for time in occ["5 Minutes"]:
        times.append(datetime.strptime(time, '%m/%d/%Y %H:%M'))

    print("Comparing evolution of Speed vs Occupancy")
    fig, ax_list = plt.subplots(2, 3) 
    ax_list[0,0].plot(times, speed["Speed (mph)"], label="speed")
    ax_list[0,0].plot(times, occ["Occupancy (%)"], label="occ")
    ax_list[0,0].legend()
    ax_list[0,0].set_title("Total")
    ax_list[0,1].plot(times, speed["Lane 1 Speed (mph)"], label="speed")
    ax_list[0,1].plot(times, occ["Lane 1 Occ (%)"], label="occ")
    ax_list[0,1].legend()
    ax_list[0,1].set_title("Lane 1")
    ax_list[0,2].plot(times, speed["Lane 2 Speed (mph)"], label="speed")
    ax_list[0,2].plot(times, occ["Lane 2 Occ (%)"], label="occ")
    ax_list[0,2].legend()
    ax_list[0,2].set_title("Lane 2")
    ax_list[1,0].plot(times, speed["Lane 3 Speed (mph)"], label="speed")
    ax_list[1,0].plot(times, occ["Lane 3 Occ (%)"], label="occ")
    ax_list[1,0].legend()
    ax_list[1,0].set_title("Lane 3")
    ax_list[1,1].plot(times, speed["Lane 4 Speed (mph)"], label="speed")
    ax_list[1,1].plot(times, occ["Lane 4 Occ (%)"], label="occ")
    ax_list[1,1].legend()
    ax_list[1,1].set_title("Lane 4")
    ax_list[1,2].plot(times, speed["Lane 5 Speed (mph)"], label="speed")
    ax_list[1,2].plot(times, occ["Lane 5 Occ (%)"], label="occ")
    ax_list[1,2].legend()
    ax_list[1,2].set_title("Lane 5")
    plt.suptitle("Occupancy vs Speed")
    

def clusterKMeans(array1, array2, nclusters):
    X = [];
    for i in range(len(array1)):
        
        X.append([array1.values[i], array2.values[i]])
        
    tags = KMeans(n_clusters=nclusters, random_state=0).fit_predict(X)
    print("Calinski-Harabaz Index: ", metrics.calinski_harabaz_score(X, tags))
    return tags
    
    
"""
    Parameter nclusters will be ignored
"""
def clusterDBScan(array1, array2, nclusters):
    X = [];
    for i in range(len(array1)):
        X.append([array1[i], array2[i]])
        
    tags = DBSCAN().fit_predict(X)
    print("Calinski-Harabaz Index: ", metrics.calinski_harabaz_score(X, tags))
    return tags
    
"""
    Will use the method passed as argument for clusterizing the data
    and then it will represent it
"""
def clusterFlowVsDensity(occ, flow, nclusters, method):    
    fig, ax_list2 = plt.subplots(3, 3) 
    occ_tags = ["Occupancy (%)", "Lane 1 Occ (%)", "Lane 5 Occ (%)"]
    flow_tags = ["Flow (Veh/5 Minutes)", "Lane 1 Flow (Veh/5 Minutes)",
                 "Lane 5 Flow (Veh/5 Minutes)"]
    speed_tags = ["Speed (mph)", "Lane 1 Speed (mph)", "Lane 2 Speed (mph)"]
    
    if method == "kmeans":
        clusterMethod = clusterKMeans
        title = "K-Means with " + str(nclusters) + " clusters."
    elif method == "DBscan":
        clusterMethod = clusterDBScan
        title = method
    else:
        print("Error: unknown cluster method")
        return   

    print("Calculating tags with speed/occ and clusterizin flow/occ")
    i = 0
    tags = []
    for ax in ax_list2[0]:
        tags.append(clusterMethod(occ[occ_tags[i]], flow[speed_tags[i]], nclusters))
        ax.scatter(occ[occ_tags[i]], flow[flow_tags[i]], c=tags[i])
        ax.set_xlabel(occ_tags[i])
        ax.set_ylabel(flow_tags[i])
        i += 1
    
    print("Using calculted tags (speed/occ) for clusterizing speed/occ")
    i = 0
    for ax in ax_list2[1]:
        ax.scatter(occ[occ_tags[i]], flow[speed_tags[i]], c=tags[i])
        ax.set_xlabel(occ_tags[i])
        ax.set_ylabel(speed_tags[i])
        i += 1
        
    print("Calculating tags with flow/occ and clusterizing flow/occ")
    i = 0
    for ax in ax_list2[2]:
        tags = clusterMethod(occ[occ_tags[i]], flow[flow_tags[i]], nclusters)

        ax.scatter(occ[occ_tags[i]], flow[flow_tags[i]], c=tags)
        ax.set_xlabel(occ_tags[i])
        ax.set_ylabel(flow_tags[i])
        i += 1 
    plt.suptitle(title)


def getIntervalData(interval, data, data_dates, date):
    if interval == "hour":
        return data[(data_dates >= date-pd.DateOffset(hours=1)) &
                    (data_dates <= date+pd.DateOffset(hours=1))]
    else:
         return data[data_dates.day==date.day]
        

def plotAccidentsData(interval, accs, occ, speed):
    accs_dates = pd.DatetimeIndex(accs.acc_date.unique())
    occ_dates = pd.DatetimeIndex(occ['5 Minutes'])
    speed_dates = pd.DatetimeIndex(speed['5 Minutes'])    
        
    i = 0
    for date in accs_dates:
        if i == MAX_PLOTS:
            break
        
        fig, ax_list = plt.subplots(2, 3) 
        interval_occ = getIntervalData(interval, occ, occ_dates, date)
        interval_speed = getIntervalData(interval, speed, speed_dates,date)
        plotOcc(interval_occ, ax=ax_list[0])
        plotSpeed(interval_speed, ax=ax_list[1])
        plotOcc(occ[occ_dates==date], ax=ax_list[0], marker='o',
                date=date.strftime('%Y-%m-%d %H:%M'))        
        plotSpeed(speed[speed_dates==date], ax=ax_list[1], marker='o',
                  date=date.strftime('%Y-%m-%d %H:%M')) 
        
        i += 1


def analyzeTrafficPerWeek():
    accidents = pd.read_excel(CRASH_PATH)
    occ_data = pd.read_table(OCC_PATH)
    speed_data = pd.read_table(SPEED_PATH)
    plotOcc(occ_data)
    plotSpeed(speed_data) 
    plotSpeedVsOcc(occ_data, speed_data)
    clusterFlowVsDensity(occ_data, speed_data, 2, "kmeans")
    clusterFlowVsDensity(occ_data, speed_data, 3, "kmeans")
    clusterFlowVsDensity(occ_data, speed_data, 5, "kmeans")
    clusterFlowVsDensity(occ_data, speed_data, 2, "DBscan")
    
    
def startAndEndDate(month):
    if month == "August":
        return '2006-08-01 00:00', '2006-08-31 23:59'
    elif month == "September":
        return '2006-09-01 00:00', '2006-09-30 23:59'
    elif month == "October":
        return '2006-10-01 00:00', '2006-10-31 23:59'
    elif month == "November":
        return '2006-11-01 00:00', '2006-11-30 23:59'
    elif month == "December":
        return '2006-12-01 00:00', '2006-12-31 23:59'
    else:
        return ('','')
    
"""
    - month: month hich will be analysed
    
    - interval: time interval before and after the accident
                Only "hour" is currently supported

    - severity: minimum accident severity
"""
def analyzeAccidents(month, interval, severity=4):
    startDate, endDate = startAndEndDate(month)
    
    accidents = read_accidents(startDate, endDate, severity)    
    occ_data = read_accident_occ(month)
    speed_data = read_accident_speed(month) 
    plotAccidentsData(interval, accidents, occ_data, speed_data)
    #clusterFlowVsDensity(occ_data, speed_data, 2, "kmeans")
    
"""
    Note: the first day of the April week is 5 -> Saturday
    Months of accident data are: August, September October, November, December
"""
if __name__ == "__main__":
    analyzeTrafficPerWeek()
    analyzeAccidents("November", "hour", 2)
    plt.show()
