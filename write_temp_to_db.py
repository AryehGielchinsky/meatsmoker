#!/usr/bin/python
import time
from gpiozero import MCP3008
#from math import log
import pymysql.cursors
from datetime import datetime as dt
import signal 
import os
import numpy as np




def get_adc_value():
    for pos in range(0,8):
        if pos not in adcs:
            adcs[pos] = MCP3008(pos)
    vals = np.array([adcs[pos].value for pos in range(0,8)])
    vals[vals > .985] = None
    return vals


def get_temp_percent():
    x = np.zeros((8,5))
    for i in range(0, 5):
        x[:,i] = get_adc_value()
        time.sleep(.2)
    return np.average(x,axis = 1)



def get_resistance(temp_percent, r=46000):
    return r*temp_percent/(1-temp_percent)


def get_temp(R):
    A = 0.6872188391*10**-3
    B = 2.103627383*10**-4
    C = 0.5449073998*10**-7

    T = (A +B*np.log(R)+C*(np.log(R)**3) )**-1
    T = T*(9/5) - 459.67
    return(T)




def write_data(temp):
 #   temp[temp is np.nan] = 'null'
    try:
        cursor = connection.cursor()
        local_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """insert into recorded_data (Smoke_Session_Id, Date_Time, Temp0, Temp1, Temp2, Temp3, Temp4, Temp5, Temp6, Temp7)
                  values (13, '{}', {}, {}, {}, {}, {}, {}, {}, {})""".format(local_time, temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])
        cursor.execute(sql)
            # connection is not autocommit by default. So you must commit to save your changes.
        connection.commit()
    except Exception as inst:
        print('write_date {}'.format(inst) )


    

adcs = {}

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


while True:

    print('Start')
    
    temp_percent = get_temp_percent()
    
    resistance = get_resistance(temp_percent = temp_percent)
    
    temp = get_temp(R = resistance)
    temp = temp.tolist()    
    temp = ['null' if (np.isnan(_)) else _ for _ in temp]

    print(temp)

    write_data(temp)
    print('Data Written')
              
    time.sleep(10)
    print('Sleep time over')
    print('')

