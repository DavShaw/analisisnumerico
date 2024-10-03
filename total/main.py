import time
import _thread
from machine import Pin, time_pulse_us, ADC

DATA = {
  "triggerPin": 27,
  "echoPin": 22,
  "temperatureSensorPin": 34,
  "ledFullPin": 26,
  "ledEmptyPin": 25,
  "ledStopPin": 5,
  "buttonFillPin": 15,
  "buttonEmptyPin": 14,
  "buttonStopPin": 19,
  "containerMaxLvl": 100,
  "maxHeight": 80,
  "minHeight": 10,
  "tempMax": 50
}

class UltrasonicSensor:
  def __init__(self):
    self.trigger = Pin(0, Pin.OUT)
    self.echo = Pin(0, Pin.IN)
    self.distanceM = 0 
    self.calibrationFactor = 1
    self.trigger.value(0)

  def setTriggerPin(self, triggerPin):
    self.trigger = Pin(triggerPin, Pin.OUT)
  
  def setEchoPin(self, echoPin):
    self.echo = Pin(echoPin, Pin.IN)

  def __calculateDistance(self):
    self.trigger.value(1)
    time.sleep_us(10)
    self.trigger.value(0)

    pulseDuration = time_pulse_us(self.echo, 1, 30000) 

    if pulseDuration < 0:
      print("ECHO TIMEOUT... Trying again.")
      self.distanceM = None
    else:
      soundVelocity = 0.0343
      self.distanceM = (pulseDuration * soundVelocity / 2) * self.calibrationFactor

    return self.distanceM

  def getDistance(self):
    distance = self.__calculateDistance()
    if distance is not None:
      print(f"Distance: {(distance)}cm")
      return distance
    print("Cannot get distance... Trying again.")
    
class TemperatureSensor:
  def __init__(self):
    self.adc = None

  def setAdcPin(self, adcPin):
    self.adc = ADC(Pin(adcPin))
    self.adc.atten(ADC.ATTN_11DB) 
    self.adc.width(ADC.WIDTH_12BIT)

  def getTemperature(self):
    adcValue = self.adc.read()
    voltage = adcValue * 5.0 / 4095
    temperatureC = voltage * 100
    return temperatureC
  
class Pulser:
  def __init__(self):
    self.lastTime = 0
    self.debounceDelay = 200

  def setAction(self, action):
    self.action = action

  def setPin(self, pinNum):
    self.pin = Pin(pinNum, Pin.IN, Pin.PULL_UP)
    self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.callback)

  def setLogic(self, logic):
    self.logic = logic

  def callback(self, a):
    currentTime = time.ticks_ms()
    if currentTime - self.lastTime > self.debounceDelay:
      try:
        getattr(self.logic, self.action)()
      except Exception as e:
        print(f"Error: {e}")
      self.lastTime = currentTime
class Logic:
  def __init__(self):
    self.ledFull = Pin(DATA["ledFullPin"], Pin.OUT)
    self.ledEmpty = Pin(DATA["ledEmptyPin"], Pin.OUT)
    self.ledStop = Pin(DATA["ledStopPin"], Pin.OUT)
    self.ledFull.off()
    self.ledEmpty.off()
    self.ledStop.off()

  def setUltraSonicSensor(self, ultrasonicSensor):
    self.ultrasonicSensor = ultrasonicSensor
  
  def setTemperatureSensor(self, temperatureSensor):
    self.temperatureSensor = temperatureSensor

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

  def startProcess(self):
    while True:
      try:
        distance = self.ultrasonicSensor.getDistance()
        temperature = self.temperatureSensor.getTemperature()
        print(f"Temperature: {temperature:.2f} °C")
        if temperature > DATA["tempMax"]:
          print("Temperature exceeds the limit! Stopping all processes...")
          self.panicStop()
        if distance is not None:
          waterLevel = (DATA["containerMaxLvl"] - distance)
          if waterLevel > DATA["maxHeight"]: # HERE (water level) MAX
            self.ledFull.off()
            print(f"Max. Water level hit ({waterLevel})")
          if waterLevel < DATA["minHeight"]: # HERE (water level) MIN
            self.ledEmpty.off()
            print(f"Min. Water level hit ({waterLevel})")
        time.sleep(1)
      except Exception as e:
        print(f"Error: {e}")
      
if __name__ == "__main__":
  ultrasonicSensor = UltrasonicSensor()
  ultrasonicSensor.setEchoPin(DATA["echoPin"])
  ultrasonicSensor.setTriggerPin(DATA["triggerPin"])

  temperatureSensor = TemperatureSensor()
  temperatureSensor.setAdcPin(DATA["temperatureSensorPin"])

  Logic = Logic()
  Logic.setUltraSonicSensor(ultrasonicSensor)
  Logic.setTemperatureSensor(temperatureSensor)

  buttonFill = Pulser() 
  buttonFill.setPin(DATA["buttonFillPin"])
  buttonFill.setLogic(Logic)
  buttonFill.setAction('containerFill')

  buttonEmpty = Pulser()
  buttonEmpty.setPin(DATA["buttonEmptyPin"])
  buttonEmpty.setLogic(Logic)
  buttonEmpty.setAction('containerEmpty')

  buttonStop = Pulser()
  buttonStop.setPin(DATA["buttonStopPin"])
  buttonStop.setLogic(Logic)
  buttonStop.setAction('panicStop')

  _thread.start_new_thread(Logic.startProcess, ())

  while True:
    time.sleep(2)
