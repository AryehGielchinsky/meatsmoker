#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:03:08 2018

@author: aryeh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql.cursors
import requests
from datetime import datetime
import time




def get_data(connection):
    with connection.cursor() as cursor:
        sql = """
            select 
                Date_Time as DT,
                Temp0,
                Temp1
            from recorded_data 
            where Smoke_Session_Id = 11
            """
        cursor.execute(sql)
        result = pd.DataFrame(cursor.fetchall())
        connection.close()
    return result


def print_data(result):
    plt.figure(figsize=(15,15))
    plt.subplot(211)
    plt.grid()
    plt.plot(result['DT'], result['Temp0'])
    plt.subplot(212)
    plt.grid()
    plt.plot(result['DT'], result['Temp1'])
    plt.ylim(ymax=260)
    plt.show()
    

#this sends a message to an app called automate. you can customize the reponse in the app
def vibrate_phone(msg):
    stuff = {
        "secret": mysql_info['secret'],
        "to": mysql_info['to'],
        "device": None,
        "payload": msg
        }
    requests.post('https://llamalab.com/automate/cloud/message', data = stuff)


def check_limits(x):
    T0 = x.tail(5).mean().Temp0
    T1 = x.tail(5).mean().Temp1
    
    if T0 > 270:
        vibrate_phone('T0 = {} > 270'.format(T0))
    elif T0 < 240:
        vibrate_phone('T0 = {} < 240'.format(T0))
    elif T1 > 197:
        vibrate_phone('T1 = {} > 197'.format(T1))


#if the meat temperature slows down (The Stall) you can wrap it in tin foil to speed it up.
#I started adding support for stall detection, but I think the meat tastes better if you leave it alone
def check_stall():
    diff = x.tail(1).head(1).Temp1.values-x.tail(85).head(1).Temp1.values
    #about half an hour of change
    if diff < 1.5:
        stalled = 1
        vibrate_phone('temp diff = {} < 1.5'.format(diff))




#get DB and automate app info
import os
mysql_info = {}
with open(os.path.expanduser('~/passwords/meat_smoker_mysql_info.txt')) as f:
    for line in f:
       (key, val) = line.split()
       mysql_info[key] = val

# Connect to the database
connection = pymysql.connect(host=mysql_info['host'],
                            user=mysql_info['user'],
                            password=mysql_info['password'],
                            db=mysql_info['db'],
                            cursorclass=pymysql.cursors.DictCursor)


stalled = 1
print('automate_cloud started')
while True:
    x = get_data(connection = connection)
    #x.Temp1[x.Temp1 >210] = np.nan
    #x.Temp0[x.Temp1 >275] = np.nan
    
    #print_data(x)
    check_limits(x)
    if stalled == 0:
        check_stall()
    
    #print(x.tail(15))
    time.sleep(30)







