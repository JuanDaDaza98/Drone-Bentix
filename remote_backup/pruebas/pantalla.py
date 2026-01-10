import RPi.GPIO as GPIO
import subprocess
import time

# Configura el pin del interruptor
INTERRUPTOR_PIN = 17  # Cambia esto por el pin que uses
ESTADO_PANTALLA = True  # True = encendida, False = apagada

GPIO.setmode(GPIO.BCM)
GPIO.setup(INTERRUPTOR_PIN, GPIO.IN)

# Comandos
def apagar_pantalla():
    subprocess.run(["wlr-randr", "--output", "HDMI-A-1", "--off"])

def encender_pantalla():
    subprocess.run(["wlr-randr", "--output", "HDMI-A-1", "--on", "--transform", "90"])

# Espera a una pulsación
print("Esperando pulsaciones en el interruptor...")

try:
    while True:
        if GPIO.input(INTERRUPTOR_PIN) == GPIO.LOW:
            if ESTADO_PANTALLA:
                print("Apagando pantalla...")
                apagar_pantalla()
                ESTADO_PANTALLA = False
            else:
                print("Encendiendo pantalla...")
                encender_pantalla()
                ESTADO_PANTALLA = True

            # Esperar a que se suelte el botón para evitar rebotes
            while GPIO.input(INTERRUPTOR_PIN) == GPIO.LOW:
                time.sleep(0.05)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Saliendo...")
finally:
    GPIO.cleanup()
