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
    x.drop('dt', axis=1, inplace=True)
    T0 = x.tail(5).mean().temp0
    T1 = x.tail(5).mean().temp1
    T2 = x.tail(5).mean().temp2
    T3 = x.tail(5).mean().temp3
    if (T0 > 275 or T0<225):
        vibrate_phone('Smoker Temp = {} !!'.format(T0))
    elif T1 > 195:
        vibrate_phone('Meat Temp1 = {} !!'.format(T1)) 
    elif T2 > 195:
        vibrate_phone('Meat Temp2 = {} !!'.format(T2))
    elif T3 > 195:
        vibrate_phone('Meat Temp3 = {} !!'.format(T3))
     



#if the meat temperature slows down (The Stall) you can wrap it in tin foil to speed it up.
#I started adding support for stall detection, but I think the meat tastes better if you leave it alone
def check_stall():
    diff = x.tail(1).head(1).temp1.values-x.tail(85).head(1).temp1.values
    #about half an hour of change
    if diff < 1.5:
        stalled = 1
        vibrate_phone('temp diff = {} < 1.5'.format(diff))



stalled = 1
print('automate_cloud started')


vibrate_phone('Connection to phone is working')

connection, login_info = get_connection()

Smoke_Session_ID = get_smoke_session(connection)

while True:
    
    x = get_data()
    
    check_limits(x)
    if stalled == 0:
        check_stall()
    
    #print(x.tail(15))
    time.sleep(10)
    print('end of loop')







