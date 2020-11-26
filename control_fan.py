from gpiozero import PWMOutputDevice as pwm
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from datetime import datetime as dt
from my_functions import get_last_smoke_session_id, get_connection, read_data, hit_db


def write_data(smoke_session_id, curr_temp, desired_temp, dc, connection):
    local_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = """insert into PWM (smoke_session_id, date_time, curr_temp, desired_temp, duty_cycle_p, duty_cycle_i, duty_cycle_d, duty_cycle)
             values ({}, '{}', {}, {}, {}, {}, {}, {})
             """.format(smoke_session_id, local_time, curr_temp, desired_temp, dc['p'], dc['i'], dc['d'], dc['total'])
    hit_db(sql, connection)



if __name__ == "__main__":
    
    factory = PiGPIOFactory()
    fan = pwm(pin = 4, initial_value = 1.0, frequency = 25000, pin_factory = factory)
    
    connection, login_info = get_connection()
    smoke_session_id = get_last_smoke_session_id(connection)
    
    desired_temp = float(input("Input desired smoker temp: "))
    print("Smoker temp will be set to {}".format(desired_temp))
    
    k={} # the PID variables
    k['p'] = 1/25
    k['i'] = 1/100
    k['d'] = -10
    
    dc = {} # duty cycle
    
    while True:
        print('Start fan controller')
        #temperature control will be achieved with PID controller logic.
        #The fan strength will be detirmined by the error between the smoker temperature and
        #the desired temperature.

        
        temp_data = read_data('recorded_data', smoke_session_id, connection)
        temp_data = temp_data[['date_time', 'temp0']].rename(columns={"temp0": "smoker_temp"})
        
        temp_data = temp_data.tail(50) # this should be time based and the intergral should be longer and the deriv shorter
        #print('curr_temp={}'.format(curr_temp))
        current_temp = temp_data.smoker_temp.iloc[-1]
        
        dc['p'] = k['p']*(desired_temp - current_temp) 
    
        dc['i'] = k['i'] * (desired_temp-temp_data['smoker_temp']).sum()/len(temp_data)
    
        dc['d'] = (k['d'] * temp_data['smoker_temp'].diff()
                            /temp_data['date_time'].diff().dt.seconds).mean()
    
        dc['total'] = dc['p'] + dc['i'] + dc['d']
        
        print('unmodded duty cycle valuea: {}'.format(dc))
    
        dc['total'] = min(dc['total'], 1)
        dc['total'] = max(dc['total'],0)
        print('actual duty_cycle: {}'.format(dc['total']))
        print('Current temp={}'.format(current_temp))
        print('')
        fan.value = dc['total']
        
        write_data(smoke_session_id, current_temp, desired_temp, dc, connection)
        sleep(10)
    
        #fan.close()
        
    
    
    
