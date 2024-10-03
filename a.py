from machine import Pin, time_pulse_us, ADC
import _thread
import time
import sys
MAX_ALTURA = 60
MIN_ALTURA = 15
TEMP_MAX = 20

# Clase para manejar el sensor ultrasónico
class SensorUltrasonico:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.distancia_cm = 0  # Variable para almacenar la distancia medida
        self.factor_calibracion = 1  # Factor de calibración

        # Inicializar el trigger en bajo
        self.trigger.value(0)

    def medir_distancia(self):
        # Enviar un pulso de 10us al pin de trigger
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)

        # Medir el tiempo del pulso de echo en microsegundos
        duracion_pulso = time_pulse_us(self.echo, 1, 30000)  # Tiempo máximo de espera: 30ms (30000us)

        if duracion_pulso < 0:  # Si duracion_pulso es negativo, indica un error o timeout
            print("Error: No se recibió el pulso del echo.")
            self.distancia_cm = None
        else:
            # Calcular la distancia en cm usando la fórmula y el factor de calibración
            self.distancia_cm = (duracion_pulso * 0.0343 / 2) * self.factor_calibracion
            self.distancia_cm += 1
            
        return self.distancia_cm

    def imprimir_distancia(self):
        # Método para medir e imprimir la distancia en consola
        distancia = self.medir_distancia()
        if distancia is not None:
            print(f"Distancia medida: {distancia:.2f} cm")
        else:
            print("No se pudo medir la distancia.")
        return distancia
    

class SensorTemperatura:
    def __init__(self, pin_adc):
        self.adc = ADC(Pin(pin_adc))
        self.adc.atten(ADC.ATTN_11DB)  # Configurar la atenuación para permitir lecturas de hasta 3.3V
        self.adc.width(ADC.WIDTH_12BIT)  # Configurar el ADC a 12 bits (rango de 0 a 4095)

    def leer_temperatura(self):
        # Leer el valor del ADC y convertirlo a voltaje
        valor_adc = self.adc.read()  # Valor ADC entre 0 y 4095

        # Ajuste de voltaje para 5V en lugar de 3.3V
        voltaje = valor_adc * 5.0 / 4095  # Convertir a voltaje (5V es el valor máximo)

        # Calibrar el cálculo de la temperatura según el sensor que estés utilizando
        # Para un LM35, la salida es de 10mV por grado Celsius
        temperatura_c = voltaje * 100  # LM35: 10mV por grado Celsius
        
        return temperatura_c


# Clase para manejar el control de LEDs y procesos
class ControlProceso:
    def __init__(self, sensor_ultrasonico, sensor_temperatura):
        # Configurar LEDs como salidas
        self.led_lleno = Pin(26, Pin.OUT)   # LED para llenado
        self.led_vacio = Pin(25, Pin.OUT)   # LED para vaciado
        self.led_paro = Pin(5, Pin.OUT)     # LED de paro o alarma
        self.sensor_ultrasonico = sensor_ultrasonico
        self.sensor_temperatura = sensor_temperatura
        # Inicializar LEDs apagados
        self.led_lleno.off()
        self.led_vacio.off()
        self.led_paro.off()

    # Métodos para manejar el proceso de llenado, vaciado y paro
    def llenar(self):
        print("[INFO] LLENADO INICIADO.")
        self.led_lleno.on()
        self.led_vacio.off()
        self.led_paro.off()

    def vaciar(self):
        print("[INFO] VACIADO INICIADO.")
        self.led_lleno.off()
        self.led_vacio.on()
        self.led_paro.off()

    def parar(self):
        print("[EMERGENCY] PARADO DE EMERGENCIA")
        self.led_lleno.off()
        self.led_vacio.off()
        self.led_paro.on()
        sys.exit(0)

    def monitorear_nivel(self):
        while True:
            distancia = self.sensor_ultrasonico.imprimir_distancia()
            temperatura = self.sensor_temperatura.leer_temperatura()
            print(f"Temperatura: {temperatura:.2f} °C")
            if temperatura > TEMP_MAX:
                print("[INFO] EXCESO DE TEMPERATURA, DETENIENDO TODOS LOS PROCESOS.")
                self.parar()
            if distancia is not None:
                if distancia >= MAX_ALTURA:  # 0.75m en cm
                    self.led_lleno.off()  # Apagar LED de llenado
                    print("[INFO] ALTURA MAXIMA EXCEDIDA (60 cm)")
                if distancia <= MIN_ALTURA:  # 0.15m en cm
                    self.led_vacio.off()  # Apagar LED de vaciado
                    print("[INFO] ALTURA MIN EXCEDIDA (10 cm)")
            time.sleep(1)  # Chequeo cada segundo

# Clase para manejar los botones y eventos con manejo de rebotes
class Boton:
    def __init__(self, pin_num, control_proceso, accion):
        # Inicializar botón y asignar el callback
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.accion = accion
        self.control_proceso = control
        self.ultimo_tiempo = 0  # Para manejar el debouncing
        self.debounce_delay = 200  # Tiempo en ms para ignorar rebotes
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.callback)  # Configurar interrupción

    def callback(self, pin):
        # Manejo de rebote: verificar el tiempo desde la última interrupción
        tiempo_actual = time.ticks_ms()
        if tiempo_actual - self.ultimo_tiempo > self.debounce_delay:
            # Ejecutar la acción asociada al botón
            print(f"Botón presionado en pin {pin}")
            getattr(self.control_proceso, self.accion)()
            self.ultimo_tiempo = tiempo_actual  # Actualizar el tiempo de la última interrupción

# Instanciar la clase del sensor ultrasónico
sensor_ultrasonico = SensorUltrasonico(trigger_pin=27, echo_pin=22)
sensor_temperatura = SensorTemperatura(pin_adc=34)

# Instanciar la clase de control de proceso
control = ControlProceso(sensor_ultrasonico, sensor_temperatura)

# Crear instancias de Botón y asociarlas a las acciones correspondientes
boton_llenar = Boton(pin_num=15, control_proceso=control, accion='llenar')   # Botón para llenar
boton_vaciar = Boton(pin_num=14, control_proceso=control, accion='vaciar')   # Botón para vaciar
boton_paro = Boton(pin_num=17, control_proceso=control, accion='parar')      # Botón para paro

# Hilo para monitorear el nivel
_thread.start_new_thread(control.monitorear_nivel, ())

# Bucle principal vacío (hilos gestionan el sensor y las interrupciones)
while True:
    time.sleep(1)
