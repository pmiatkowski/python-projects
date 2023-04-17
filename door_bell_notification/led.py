from machine import Pin, Timer

class Led:
    isBlinking = False
    timer = Timer(-1)
    
    def __init__(self, ledPin=15, period=100):
        self.ledPin = ledPin
        self.led = Pin(self.ledPin, Pin.OUT)
        self.period = period
    
    def on(self):
        self.stopBlinking()
        self.led.value(1)
        
    def off(self):
        self.stopBlinking()
        self.led.value(0)
        
    def toggle(self):
        self.stopBlinking()
        self.led.toggle()
        
    def startBlinking(self, overridePeriod=None):
        def f(timer):
            if self.isBlinking:
                self.led.toggle()
            else:
                timer.deinit()
        p = self.period
        if overridePeriod is not None:
            p = overridePeriod
        
        if not self.isBlinking:            
            self.timer.init(period=p, callback=f)
            self.isBlinking = True
            
    def stopBlinking(self):
        if self.isBlinking:
            self.timer.deinit()
            self.isBlinking = False

