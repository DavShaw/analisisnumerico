from pulser import Pulser
from logic import Logic
from ultra import UltrasonicSensor
from temp import TemperatureSensor
from data import DATA
import time
import _thread
if __name__ == "__main__":
  ultrasonicSensor = UltrasonicSensor()
  ultrasonicSensor.setEchoPin(DATA["echoPin"])
  ultrasonicSensor.setTriggerPin(DATA["triggerPin"])

  temperatureSensor = TemperatureSensor()
  temperatureSensor.setPin(DATA["tempPin"])

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
