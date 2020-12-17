#!/usr/bin/python
import time
from gpiozero import MCP3008
import numpy as np


def get_adc_value():
    for pos in range(0,4):
        if pos not in adcs:
            adcs[pos] = MCP3008(pos)
    vals = np.array([adcs[pos].value for pos in range(0,4)])
#    vals[vals > .985] = None
    return vals

def get_temp_percent():
    x = np.zeros((4,5))
    for i in range(0, 5):
        x[:,i] = get_adc_value()
        time.sleep(.2)
    return np.average(x,axis = 1)


adcs={}
while True:
    # print(get_temp_percent()) 
    print(time.strftime("%H:%M:%S", time.localtime()))
    print(get_adc_value())
    time.sleep(1)
    print('')

