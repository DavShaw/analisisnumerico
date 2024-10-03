from machine import Pin, time_pulse_us
import time

class UltrasonicSensor:
  def __init__(self):
    self.distanceM = 0 
    self.calibrationFactor = 0.45 
    self.trigger.value(0)

  def setTriggerPin(self, triggerPin):
    self.trigger = Pin(triggerPin, Pin.OUT)
  
  def setEchoPin(self, echoPin):
    self.echo = Pin(echoPin, Pin.IN)

  def measureDistance(self):
    self.trigger.value(1)
    time.sleep_us(10)
    self.trigger.value(0)

    pulseDuration = time_pulse_us(self.echo, 1, 30000) 

    if pulseDuration < 0:
      print("ECHO TIMEOUT... Trying again.")
      self.distanceM = None
    else:
      soundVelocity = 343
      self.distanceM = (pulseDuration * soundVelocity / 2) * self.calibrationFactor

    return self.distanceM

  def printDistance(self):
    distance = self.measureDistance()
    if distance is not None:
      print(f"Distance: {(distance/100)}m")
    else:
      print("Cannot get distance... Trying again.")
    return distance