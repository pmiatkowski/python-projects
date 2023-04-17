from machine import Pin, Timer, reset
from led import Led
import time


class Reset:
    def __init__(self, button_pin=14, wait=3):
        self.button_pin = button_pin
        self.button = Pin(self.button_pin, Pin.IN, Pin.PULL_DOWN)
        self.wait = wait
        self.timer = Timer()
        self.timer.init(period=2000, callback=self.reset)
        self.led = Led()
        
    def reset(self, timer):
        if self.button.value():
            print('Resetting machine in', self.wait, 's.')
            self.led.off()
            timer.deinit()
            time.sleep(self.wait)
            reset()
        
