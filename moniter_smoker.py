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
from my_functions import get_smoke_session
from my_functions import get_connection


def read_data(Smoke_Session_ID, read_type = 'PWM'):
    try:
        if read_type == 'PWM':
            table_name = 'PWM' 
        elif read_type == 'smoker_temps':
            table_name = 'recorded_data' 
        else:
            print('read_data_PWM neads a table name')
        cursor = connection.cursor()
        sql = """select * 
                from {}
                where smoke_session_id = {}
                """.format(table_name, Smoke_Session_ID)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as inst:
        print('read_data {}'.format(inst) )
        

     
        
connection, login_info = get_connection()

Smoke_Session_ID = get_smoke_session(connection)

hours_ago = 100000
start_time = '2018-06-28 12:00:00'

for i in range(20):
    print('')


smoker_temps_data=pd.DataFrame( read_data(Smoke_Session_ID, 'smoker_temps') )
#smoker_temps_data=smoker_temps_data[smoker_temps_data['Date_Time']
#        > (datetime.now() - timedelta(hours=hours_ago))]
smoker_temps_data=smoker_temps_data[smoker_temps_data['date_time']> start_time]

#smoker_temps_data=smoker_temps_data[smoker_temps_data['Date_Time'] > '2018-06-04 19:46:00']


PWM_data=pd.DataFrame( read_data(Smoke_Session_ID, 'PWM') )
PWM_data=PWM_data[PWM_data['date_time']> (datetime.now() - timedelta(hours=hours_ago))]
PWM_data=PWM_data[PWM_data['date_time']> start_time]


#div_temp = smoker_temps_data['Temp0'].diff()/smoker_temps_data['Date_Time'].diff().dt.seconds
#
#plt.figure(figsize=(14, 6))
#plt.plot(smoker_temps_data['Date_Time'], div_temp, '.')
#plt.grid() 


plt.figure(figsize=(14, 14))
plt.subplot(411)
plt.plot(smoker_temps_data['date_time'], smoker_temps_data['temp0'], label='smoker')
plt.plot(smoker_temps_data['date_time'], smoker_temps_data['temp1'], '.', label='meat1')
plt.plot(smoker_temps_data['date_time'], smoker_temps_data['temp2'], '.', label='meat2')
plt.grid()  
plt.legend(loc = 'upper left')
plt.xlabel('Time')
plt.ylabel('temp')
plt.title('main')



plt.subplot(412)
plt.plot(PWM_data['date_time'], PWM_data['curr_temp'], label = 'smoker secondary')
plt.plot(smoker_temps_data['date_time'], smoker_temps_data['temp0'], '.', label='smoker primary')
plt.plot(PWM_data['date_time'], PWM_data['desired_temp'], label='desired temp')
plt.legend(loc = 'upper left')
plt.grid()  
plt.xlabel('Time')
plt.ylabel('smoker temp')



plt.subplot(413)
plt.plot(PWM_data['date_time'], PWM_data['duty_cycle_p'], label='p')
plt.plot(PWM_data['date_time'], PWM_data['duty_cycle_i'], label='i')
plt.plot(PWM_data['date_time'], PWM_data['duty_cycle_d'], label='d')
plt.plot(PWM_data['date_time'], np.zeros(len(PWM_data)), label='0')
plt.legend(loc = 'upper left')
plt.grid()  
plt.xlabel('Time')
plt.ylabel('Fan duty cycle parts')

plt.subplot(414)
plt.plot(PWM_data['date_time'], PWM_data['duty_cycle'])
plt.grid()  
plt.xlabel('Time')
plt.ylabel('Fan actual duty cycle')

print(smoker_temps_data[['temp0', 'temp1', 'temp2']].tail(5) )

#print( (-z['curr_temp'].diff()/z['Date_Time'].diff().dt.seconds).mean() )
#print( ((z['Date_Time'].diff().dt.seconds)*(260-z['curr_temp'])).sum() )

