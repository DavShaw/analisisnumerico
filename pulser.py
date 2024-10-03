from machine import Pin
import time

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

  def callback(self):
    currentTime = time.ticks_ms()
    if currentTime - self.lastTime > self.debounceDelay:
      getattr(self.Logic, self.action)()
      self.lastTime = currentTime