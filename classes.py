from machine import Pin, time_pulse_us, ADC
import _thread
import time


DATA = {
  "triggerPin": 27,
  "echoPin": 22,
  "temperatureSensorPin": 34,
  "ledFullPin": 26,
  "ledEmptyPin": 25,
  "ledStopPin": 5,
  "buttonFillPin": 15,
  "buttonEmptyPin": 14,
  "buttonStopPin": 17,
  "maxHeight": 40,
  "minHeight": 10,
  "tempMax": 35
}

class UltrasonicSensor:
  def __init__(self, triggerPin, echoPin):
    self.trigger = Pin(triggerPin, Pin.OUT)
    self.echo = Pin(echoPin, Pin.IN)
    self.distanceM = 0 
    self.calibrationFactor = 1  
    self.trigger.value(0)

  def measureDistance(self):
    self.trigger.value(1)
    time.sleep_us(10)
    self.trigger.value(0)

    pulseDuration = time_pulse_us(self.echo, 1, 30000) 

    if pulseDuration < 0:
      print("ECHO TIMEOUT... Trying again.")
      self.distanceM = None
    else:
      self.distanceM = (pulseDuration * 0.0343 / 2) * self.calibrationFactor
      self.distanceM += 1

    return self.distanceM

  def printDistance(self):
    distance = self.measureDistance()
    if distance is not None:
      print(f"Distance: {(distance/100):.2f}m")
    else:
      print("Cannot get distance... Trying again.")
    return distance

class TemperatureSensor:
  def __init__(self, adcPin):
    self.adc = ADC(Pin(adcPin))
    self.adc.atten(ADC.ATTN_11DB) 
    self.adc.width(ADC.WIDTH_12BIT)

  def readTemperature(self):
    adcValue = self.adc.read()
    voltage = adcValue * 5.0 / 4095
    temperatureC = voltage * 100
    return temperatureC

class Logic:
  def __init__(self, ultrasonicSensor, temperatureSensor):
    self.ledFull = Pin(DATA["ledFullPin"], Pin.OUT)
    self.ledEmpty = Pin(DATA["ledEmptyPin"], Pin.OUT)
    self.ledStop = Pin(DATA["ledStopPin"], Pin.OUT)
    self.ultrasonicSensor = ultrasonicSensor
    self.temperatureSensor = temperatureSensor
    self.ledFull.off()
    self.ledEmpty.off()
    self.ledStop.off()

  def containerFill(self):
    print("Filling container...")
    self.ledFull.on()
    self.ledEmpty.off()
    self.ledStop.off()

  def containerEmpty(self):
    print("Emptying container...")
    self.ledFull.off()
    self.ledEmpty.on()
    self.ledStop.off()

  def panicStop(self):
    print("PANIC! Stopping all processes...")
    self.ledFull.off()
    self.ledEmpty.off()
    self.ledStop.on()

  def monitorLevel(self):
    while True:
      distance = self.ultrasonicSensor.printDistance()
      temperature = self.temperatureSensor.readTemperature()
      print(f"Temperature: {temperature:.2f} °C")
      if temperature > DATA["tempMax"]:
        print("Temperature exceeds the limit! Stopping all processes...")
        self.stop()
      if distance is not None:
        if distance >= DATA["maxHeight"]:
          self.ledFull.off()
          print(f"Max. Distance hit ({DATA["maxHeight"]})")
        if distance <= DATA["minHeight"]:
          self.ledEmpty.off()
          print(f"Min. Distance hit ({DATA["minHeight"]})")
      time.sleep(1) 

class Pulser:
  def __init__(self, pinNum, Logic, action):
    self.pin = Pin(pinNum, Pin.IN, Pin.PULL_UP)
    self.action = action
    self.Logic = Logic
    self.lastTime = 0
    self.debounceDelay = 200
    self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.callback)

  def callback(self):
    currentTime = time.ticks_ms()
    if currentTime - self.lastTime > self.debounceDelay:
      getattr(self.Logic, self.action)()
      self.lastTime = currentTime

if __name__ == "__main__":
  ultrasonicSensor = UltrasonicSensor(triggerPin=DATA["triggerPin"], echoPin=DATA["echoPin"])
  temperatureSensor = TemperatureSensor(adcPin=DATA["temperatureSensorPin"])

  Logic = Logic(ultrasonicSensor, temperatureSensor)

  buttonFill = Pulser(pinNum=DATA["buttonFillPin"], Logic=Logic, action='containerFill') 
  buttonEmpty = Pulser(pinNum=DATA["buttonEmptyPin"], Logic=Logic, action='containerEmpty') 
  buttonStop = Pulser(pinNum=DATA["buttonStopPin"], Logic=Logic, action='panicStop')

  _thread.start_new_thread(Logic.monitorLevel, ())

  while True:
    time.sleep(2)
