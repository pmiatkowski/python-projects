import utime
from machine import Pin, Timer
from wlan import WLAN
from http_socket import createSocket
from led import Led
from resetButton import Reset

# Configure leds
wlan_led_pin = 14
bell_led_pin = 13

# Configure buttons
reset_button_pin = 15

# Configure GPIO pin for speaker
speaker_pin = 4
speaker = Pin(speaker_pin, Pin.OUT)

# Setup reset button
Reset(reset_button_pin)


# Connect to Wlan
wlan = WLAN(wlan_led_pin, False)
wlan.connect()
isConnected = wlan.isConnected()
if isConnected:
    print('Connected')
    

# Configure on bell action
bell_led_timeout = 15
teardown_timer = Timer()

def on_bell_action():
    print('Action triggerred')
    teardown_timer.deinit()
    start_time = utime.time()
    led = Led(bell_led_pin)
    
    # Will tear down other timers
    def tear_down(timer):
        if utime.time() - start_time >= bell_led_timeout:
            led.off()
            timer.deinit()
    teardown_timer.init(period=1000, callback=tear_down)
    
    led.startBlinking()
    
# Create Socket listener
socketListener = createSocket(on_bell_action)
socketListener()
