#!/usr/bin/python
import time
from gpiozero import MCP3008
from datetime import datetime as dt
import numpy as np
from my_functions import get_last_smoke_session_id, get_connection, hit_db, read_data

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
    # old thermistors
    # A = 0.6872188391*10**-3
    # B = 2.103627383*10**-4
    # C = 0.5449073998*10**-7
    
    # new thermistors
    A = 1.216527419*10**-3
    B = 1.337979364*10**-4
    C = 3.947291334*10**-7

    T = (A +B*np.log(R)+C*(np.log(R)**3) )**-1
    T = T*(9/5) - 459.67
    return(T)


def write_temp(temp, smoke_session_id, connection):
    local_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = """insert into recorded_data (smoke_session_id, date_time, temp0, temp1, temp2, temp3)
             values ({}, '{}', {}, {}, {}, {} )
             """.format(smoke_session_id, local_time, temp[0], temp[1], temp[2], temp[3] )
    hit_db(sql, connection)


########################################################################################
def write_new_ss(new_ss, connection):
    sql = """insert into smoke_session (date_time, meat_type, kilos, notes)
             values (now(), '{}', '{}', '{}');
             """.format(new_ss['meat_type'], new_ss['kilos'], new_ss['notes'])
    return hit_db(sql, connection)


def check_smoke_session(connection):
        
    smoke_session_id = get_last_smoke_session_id(connection)
    
    if smoke_session_id == None:
        first_smoke = input("Is this your first smoke in this db? (y/n): ")
        if first_smoke == 'y':
            continue_ss = 'n'
        else:
            raise ValueError('I cant find any earlier smoke sessions. Try debugging.')
    else:        
        last_ss = read_data('smoke_session', smoke_session_id, connection)    
        print('Last Smoke Session is:')
        print('ID:          {}'.format(last_ss['smoke_session_id']))
        print('Start:       {}'.format(last_ss['date_time']))
        print('Meat Type:   {}'.format(last_ss['meat_type']))
        print('kilos:       {}'.format(last_ss['kilos']))
        print('notes:       {}'.format(last_ss['notes']))
        print('')        
        continue_ss = input("Do you want to continue this smoke session? (y/n): ")
    
    
    if continue_ss== 'n':
        new_ss = {}
        new_ss['meat_type'] = input('Enter meat type: ')
        new_ss['kilos'] = float(input('Enter number kilos: '))
        new_ss['notes'] = input('Enter notes: ')
        
        write_new_ss(new_ss, connection)
        smoke_session_id = get_last_smoke_session_id(connection)
        
    return smoke_session_id        
        
########################################################################################



if __name__ == "__main__":

    adcs = {}  
    
    connection, login_info = get_connection()
    smoke_session_id = check_smoke_session(connection)
    
    while True:
    
        print('Start')
        
        temp_percent = get_temp_percent()
        
        resistance = get_resistance(temp_percent = temp_percent)
        
        temp = get_temp(R = resistance)
        temp = temp.tolist()    
        temp = ['null' if (np.isnan(_)) else _ for _ in temp]
    
        print(temp)
    
        write_temp(temp, smoke_session_id, connection)
        print('Data Written')
                  
        time.sleep(1)
        print('Sleep time over')
        print('')

