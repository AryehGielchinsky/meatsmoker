from gpiozero import PWMOutputDevice as pwm
from time import sleep
import numpy as np
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import pymysql.cursors
from datetime import datetime as dt
import signal 
import os
import pandas as pd
from my_functions import get_smoke_session
from my_functions import get_connection


def read_data(Smoke_session_ID):
    try:
        cursor = connection.cursor()
        sql = """select date_time, temp0 as smoker_temp
                from recorded_data
                where smoke_session_id = {}
                """.format(Smoke_session_ID)
        cursor.execute(sql)
        result = cursor.fetchall()
        return pd.DataFrame(result)
    except Exception as inst:
        print('read_data {}'.format(inst) )

#write_data(Smoke_Session_ID, temp_data['smoker_temp'].tail(1).mean(), desired_temp, duty_cycle_p, duty_cycle_i, duty_cycle_d, duty_cycle)
def write_data(Smoke_Session_ID, curr_temp, desired_temp, duty_cycle_p, duty_cycle_i, duty_cycle_d, duty_cycle):
    try:
        cursor = connection.cursor()
        local_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """insert into PWM (smoke_session_id, date_time, curr_temp, desired_temp, duty_cycle_p, duty_cycle_i, duty_cycle_d, duty_cycle)
                  values ({}, '{}', {}, {}, {}, {}, {}, {})""".format(Smoke_Session_ID, local_time, curr_temp, desired_temp, duty_cycle_p, duty_cycle_i, duty_cycle_d, duty_cycle)
        cursor.execute(sql)
            # connection is not autocommit by default. So you must commit to save your changes.
        connection.commit()
    except Exception as inst:
        print('write_date {}'.format(inst) )


factory = PiGPIOFactory()
fan = pwm(pin = 4, initial_value = 1.0, frequency = 25000, pin_factory = factory)


#connection to MySQL db
connection, login_info = get_connection()

#smokesessionid needs to be changed manuall for now.
Smoke_Session_ID = get_smoke_session(connection)

desired_temp = float(input("Input desired smoker temp: "))
print("Smoker temp will be set to {}".format(desired_temp))

kp = .5*.5*1/25
ki = 2*1/10000
kd = .5*.5*20

#-z['curr_temp'].diff()/z['Date_Time'].diff().dt.seconds
#(z['Date_Time'].diff().dt.seconds)*(260-z['curr_temp'])

while True:
    print('Start fan controller')
    #temperature control will be achieve with PID controller logic.
    #The fan strength will be detirmined by the error between the smoker temperature and
    #the desired temperature.
    # The error itself (proportional control), the intergral of the error (intergral control)
    # and the derivative of the error (derivative controll) will be used
    
    #Date_Time, Temp0 as smoker_temp
    temp_data = read_data(Smoke_Session_ID)
    temp_data = temp_data.tail(30)
    #print('curr_temp={}'.format(curr_temp))
    duty_cycle_p = kp*(desired_temp-temp_data['smoker_temp'].tail(1).mean()) 

    duty_cycle_i = ki * ( (temp_data['date_time'].diff().dt.seconds)
                        *(desired_temp-temp_data['smoker_temp']) ).sum()

    duty_cycle_d = (-kd * temp_data['smoker_temp'].diff()
                    /temp_data['date_time'].diff().dt.seconds).mean()

    print('duty_cycle_p={}'.format(duty_cycle_p))
    print('duty_cycle_i={}'.format(duty_cycle_i))
    print('duty_cycle_d={}'.format(duty_cycle_d))

    duty_cycle = duty_cycle_p + duty_cycle_i + duty_cycle_d
    print('duty_cycle unmodded={}'.format(duty_cycle))
    duty_cycle = min(duty_cycle, 1)
    duty_cycle = max(duty_cycle,0)
    print('actual duty_cycle={}'.format(duty_cycle))
    print('Current temp={}'.format(temp_data['smoker_temp'].tail(1).mean()))
    print('')
    fan.value = duty_cycle
    
    write_data(Smoke_Session_ID, temp_data['smoker_temp'].tail(1).mean(), desired_temp, duty_cycle_p, duty_cycle_i, duty_cycle_d, duty_cycle)
    sleep(10)

    #fan.close()
    


