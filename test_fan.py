#sudo pigpiod
from gpiozero import PWMOutputDevice as pwm
from time import sleep
import numpy as np
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
fan = pwm(pin = 4, initial_value = 0, frequency = 25000, pin_factory = factory)



while True:
    fan.value=0
#    sleep(300)
#    fan.value=0
#    sleep(300)
#fan.close()
