import secrets
import network
import machine
import time
from machine import Timer
from led import Led

class WLAN:
    def __init__(self, led_pin = 15, wlanAutorestart=True, ssid=secrets.SSID, password=secrets.PASSWORD):
        self.wlanAutorestart = wlanAutorestart
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.monitorTimer = Timer()
        self.led_pin = led_pin
        self.reconnectTime = 2
        self.led = Led(self.led_pin)
        
    def setSSID(self, ssid):
        self.ssid = ssid
        return self
        
    def setPassword(self, password):
        self.password = password
        return self
    
    def setAutorestartMachine(self, autorestart):
        self.wlanAutorestart = autorestart
        return self
    
    def setReconnectTime(self, t):
        self.reconnectTime = t
        return self
    
    def setled_pin(self, pinNo):
        self.led_pin = pinNo
        return self
        
    def getLocalIp(self):
        sta_if = network.WLAN(network.STA_IF)
        if sta_if.active():
            return sta_if.ifconfig()[0]
        ap_if = network.WLAN(network.AP_IF)
        if ap_if.active():
            return ap_if.ifconfig()[0]
        return None
    
    def getMacAddress(self):
        mac = network.WLAN().config('mac')
        macAddress = ':'.join('%02x' % b for b in mac)
        return macAddress
        
    def connect(self):
        self.monitorTimer.deinit()
        self.led.startBlinking()
        print('Trying to connect to ' + self.ssid)
        
        self.wlan.connect(self.ssid, self.password)
        time.sleep(1)
        
        if self.isConnected():
            self.led.on()
            self.printConnectedMessage()
            self.monitorConnection()
            
        else:
            print('CONNECTION ERROR. Cannot connect to the network SSID: ' + self.ssid)
            self.led.startBlinking()
            if self.wlanAutorestart:
                print('Restarting device..')
                time.sleep(self.reconnectTime)
                print('Shutting down')
                machine.reset()
            else:
                time.sleep(self.reconnectTime)
                self.connect()
            
    def isConnected(self):
        return self.wlan.isconnected()
    
    def printConnectedMessage(self):
        print('Connected to: ', self.ssid)
        print('Mac address: ', self.getMacAddress())
        print('IP address: ', self.getLocalIp())
        
    def monitorConnection(self):
        def f(timer):
            if self.isConnected() is not True:
                self.monitorTimer.deinit()
                self.led.startBlinking()
                print('Error: ', e)
                print('Lost connection to the network ' + ssid + '. Trying to reconnect in 5 seconds')
                time.sleep(5)
                self.connect()
            else:
                #print('WLAN Connection status ok')
                self.led.on()
                
        self.monitorTimer.init(period=1000, callback=f)
