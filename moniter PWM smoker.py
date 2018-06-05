#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 11:07:18 2018

@author: aryeh
"""

from time import sleep
import numpy as np
import pandas as pd
import pymysql.cursors
from datetime import datetime as dt
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


#get DB info
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



def read_data(Smoke_Session_ID, read_type = 'PWM'):
    try:
        if read_type == 'PWM':
            table_name = 'PWM2' 
        elif read_type == 'smoker_temps':
            table_name = 'recorded_data' 
        else:
            print('read_data_PWM neads a table name')
        cursor = connection.cursor()
        sql = """select * 
                from {}
                where Smoke_Session_ID = {}
                """.format(table_name, Smoke_Session_ID)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as inst:
        print('read_data {}'.format(inst) )
        
        
        

Smoke_Session_ID = 17
hours_ago = 100

for i in range(5):
    print('')


smoker_temps_data=pd.DataFrame( read_data(Smoke_Session_ID, 'smoker_temps') )
smoker_temps_data=smoker_temps_data[smoker_temps_data['Date_Time']
        > (datetime.now() - timedelta(hours=hours_ago))]

smoker_temps_data=smoker_temps_data[smoker_temps_data['Date_Time'] > '2018-05-21 00:00:00']


#PWM_data=pd.DataFrame( read_data(Smoke_Session_ID, 'PWM') )
#PWM_data=PWM_data[PWM_data['Date_Time']> (datetime.now() - timedelta(hours=hours_ago))]




plt.figure(figsize=(16, 14))
plt.subplot(211)
#plt.plot(smoker_temps_data['Date_Time'], smoker_temps_data['Temp0'], label='smoker')
plt.plot(smoker_temps_data['Date_Time'], smoker_temps_data['Temp1'], '.', label='meat')
plt.grid()  
plt.xlabel('Time')
plt.ylabel('meat temp')


plt.subplot(212)
#plt.plot(PWM_data['Date_Time'], PWM_data['curr_temp'])
plt.plot(smoker_temps_data['Date_Time'], smoker_temps_data['Temp0'], '.', label='smoker')
#plt.plot(PWM_data['Date_Time'], PWM_data['desired_temp'], label='desired temp')
plt.legend()
plt.grid()  
plt.xlabel('Time')
plt.ylabel('smoker temp')


#plt.subplot(413)
##plt.plot(PWM_data['Date_Time'], PWM_data['curr_temp'])
#plt.plot(smoker_temps_data['Date_Time'], smoker_temps_data['Temp2'], label='notconnected')
##plt.plot(PWM_data['Date_Time'], PWM_data['desired_temp'], label='desired temp')
#plt.legend()
#plt.grid()  
#plt.xlabel('Time')
#plt.ylabel('smoker temp')


#plt.subplot(413)
#plt.plot(PWM_data['Date_Time'], PWM_data['duty_cycle_p'], label='p')
#plt.plot(PWM_data['Date_Time'], PWM_data['duty_cycle_i'], label='i')
#plt.plot(PWM_data['Date_Time'], PWM_data['duty_cycle_d'], label='d')
#plt.plot(PWM_data['Date_Time'], np.zeros(len(PWM_data)), label='0')
#plt.legend()
#plt.grid()  
#plt.xlabel('Time')
#plt.ylabel('duty_cycle')
#
#plt.subplot(414)
#plt.plot(PWM_data['Date_Time'], PWM_data['duty_cycle'])
#plt.grid()  
#plt.xlabel('Time')
#plt.ylabel('duty_cycle')


#print( (-z['curr_temp'].diff()/z['Date_Time'].diff().dt.seconds).mean() )
#print( ((z['Date_Time'].diff().dt.seconds)*(260-z['curr_temp'])).sum() )



