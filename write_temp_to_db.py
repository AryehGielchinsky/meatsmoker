#!/usr/bin/python
import time
from gpiozero import MCP3008
from datetime import datetime as dt
import numpy as np
from my_functions import get_smoke_session
from my_functions import get_connection

# there are 4 positions in the ADC because I have 4 temp probes ports.

def get_adc_value():
    for pos in range(0,4):
        if pos not in adcs:
            adcs[pos] = MCP3008(pos)
    vals = np.array([adcs[pos].value for pos in range(0,4)])
    vals[vals > .985] = None
    return vals


def get_temp_percent():
    x = np.zeros((4,5))
    for i in range(0, 5):
        x[:,i] = get_adc_value()
        time.sleep(.2)
    return np.average(x,axis = 1)



def get_resistance(temp_percent, r=46000):
    return r*temp_percent/(1-temp_percent)


#Steinhart–Hart equation converts resistance to temperature
def get_temp(R):
    A = 0.6872188391*10**-3
    B = 2.103627383*10**-4
    C = 0.5449073998*10**-7

    T = (A +B*np.log(R)+C*(np.log(R)**3) )**-1
    T = T*(9/5) - 459.67
    return(T)



#the frist value is smokesessionid and needs to be changed manually
def write_data(temp):
 #   temp[temp is np.nan] = 'null'
    try:
        cursor = connection.cursor()
        local_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """insert into recorded_data (smoke_session_id, date_time, temp0, temp1, temp2, temp3)
                  values ({}, '{}', {}, {}, {}, {} )""".format(Smoke_Session_ID, local_time, temp[0], temp[1], temp[2], temp[3] )
        cursor.execute(sql)
            # connection is not autocommit by default. So you must commit to save your changes.
        connection.commit()
    except Exception as inst:
        print('write_date {}'.format(inst) )



adcs = {}

connection, login_info = get_connection()

Smoke_Session_ID = get_smoke_session(connection)


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

