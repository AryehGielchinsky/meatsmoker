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
from my_functions import get_smoke_session
from my_functions import get_connection



def get_data():
    connection, login_info = get_connection()
    with connection.cursor() as cursor:
        sql = """
            select 
                date_time as dt,
                temp0,
                temp1,
                temp2,
                temp3
            from recorded_data 
            where smoke_session_id = {}
            """.format(Smoke_Session_ID)
        cursor.execute(sql)
        result = pd.DataFrame(cursor.fetchall())
        connection.close()
    return result

   

#this sends a message to an app called automate. you can customize the reponse in the app
def vibrate_phone(msg):
    connection, login_info = get_connection()
    stuff = {
        "secret": login_info['secret'],
        "to": login_info['to'],
        "device": None,
        "payload": msg
        }
    requests.post('https://llamalab.com/automate/cloud/message', data = stuff)


def check_limits(x):
    y = x.copy()
    y.drop('dt', axis=1, inplace=True)
    T0 = y.tail(5).mean().temp0
    T1 = y.tail(5).mean().temp1
    T2 = y.tail(5).mean().temp2
    T3 = y.tail(5).mean().temp3
    if (T0 > 275 or T0<225):
        vibrate_phone('Smoker Temp = {} !!'.format(T0))
    elif T1 > 200:
        vibrate_phone('Meat Temp1 = {} !!'.format(T1)) 
    elif T2 > 200:
        vibrate_phone('Meat Temp2 = {} !!'.format(T2))
    elif T3 > 200:
        vibrate_phone('Meat Temp3 = {} !!'.format(T3))
     



#if the meat temperature slows down (The Stall) you can wrap it in tin foil to speed it up.
#I started adding support for stall detection, but I think the meat tastes better if you leave it alone
def check_stall(stalled):
    diff_temp = x.tail(1).head(1).temp1.values-x.tail(100).head(1).temp1.values
    diff_time = x.tail(1).head(1).dt.iloc[0]-x.tail(100).head(1).dt.iloc[0]
    diff_time = diff_time.total_seconds()/(60*60) # in hours now
    temp_per_hour = diff_temp / diff_time
    print(temp_per_hour)
    if temp_per_hour < 4:
        stalled = 1
        vibrate_phone('temp_per_hour = {} < 1.5'.format(temp_per_hour))
    return stalled



stalled = 0
print('automate_cloud started')


vibrate_phone('Connection to phone is working')

connection, login_info = get_connection()

Smoke_Session_ID = get_smoke_session(connection)

while True:
    
    x = get_data()
    
    print('Checking Limits')
    check_limits(x)
    if stalled == 0:
        print('Checking for stall')
        stalled = check_stall(stalled)
    
    #print(x.tail(15))
    time.sleep(10)
    print('end of loop')
    print('')







