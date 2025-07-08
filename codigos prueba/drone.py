import socket
from gpiozero import LED
import time
from time import sleep
import spidev
import board
import busio
from adafruit_pca9685 import PCA9685


# Configuración del socket del servidor para recibir datos
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.4.3", 5000))  # Dirección IP del servidor
server_socket.listen(1)

print("Esperando conexión...")

# Configuración de los LEDs
led1 = LED(17)
led2 = LED(27)
led3 = LED(22)

client_socket, client_address = server_socket.accept()
print(f"Conexión recibida de {client_address}")

leds_on = False
button1_prev_state = 0
button2_prev_state = 0

# Inicialización PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz típico ESC

def us_to_duty(us):
    return int(us / 20000 * 0xFFFF)

def map_value(x):
    if x < 128:
        # mapa 0-127 a 1150-1500
        return int(1150 + (x / 127) * (1500 - 1150))
    else:
        # mapa 128-255 a 1500-1850
        return int(1500 + ((x - 128) / 127) * (1850 - 1500))

try:
    while True:
        data = client_socket.recv(1024)
        if data:
            # Convertir los datos recibidos en una lista de enteros
            joystick_data = list(map(int, data.decode().split(',')))
            y1_value,  x2_value, y2_value, button1_state, button2_state = joystick_data

            print(f"{y1_value},{x2_value},{y2_value},{button1_state},{button2_state}")

            # Control PWM motores con valores Y1 y Y2
            us_motor1 = map_value(y1_value)
            us_motor2 = map_value(y2_value)
            us_motor3 = map_value(y1_value)
            us_motor4 = map_value(y1_value)

            pca.channels[0].duty_cycle = us_to_duty(us_motor1)
            pca.channels[1].duty_cycle = us_to_duty(us_motor2)
            pca.channels[2].duty_cycle = us_to_duty(us_motor3)
            pca.channels[3].duty_cycle = us_to_duty(us_motor4)

            print(f"M1: {us_motor1} us | M2: {us_motor2} us")

            sleep(0.1)
        
        if button2_state == 1 and button2_prev_state == 0:
            if not leds_on:
                #led1.on()
                led2.on()
                led3.on()
                leds_on = True
            else:
                #led1.off()
                led2.off()
                led3.off()
                leds_on = False

except KeyboardInterrupt:

    print("\nApagando motores y cerrando conexión...")
    # Neutral para los ESC al cerrar
    pca.channels[0].duty_cycle = us_to_duty(1500)
    pca.channels[1].duty_cycle = us_to_duty(1500)

    client_socket.close()
    server_socket.close()
    pca.deinit()
