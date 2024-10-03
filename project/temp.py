from machine import ADC, Pin

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