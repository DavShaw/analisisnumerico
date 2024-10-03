from data import DATA
from machine import Pin
import time

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