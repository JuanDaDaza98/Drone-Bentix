from gpiozero import MCP3008, Button
from time import sleep

# Configuración de pines
CLK = 11
MOSI = 10
MISO = 9
CS = 13

# Joysticks
y2 = MCP3008(channel=1, clock_pin=CLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS)  # Joystick izquierdo vertical
x2 = MCP3008(channel=0, clock_pin=CLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS)  # Joystick izquierdo horizontal
y1 = MCP3008(channel=3, clock_pin=CLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS)  # Joystick derecho vertical

# Botones
button1 = Button(4)
button2 = Button(26)

print("🔧 Leyendo valores de los joysticks... (Ctrl+C para salir)")

try:
    while True:
        # Lectura analógica (escalada a 0-255)
        y1_val = int(255 - (y1.value * 255))
        x2_val = int(255 - (x2.value * 255))
        y2_val = int(y2.value * 255)

        # Estado de botones
        b1 = int(button1.is_pressed)
        b2 = int(button2.is_pressed)

        print(f"Y1 (Derecho): {y1_val} | X2 (Izquierdo): {x2_val} | Y2 (Izquierdo): {y2_val} | B1: {b1} | B2: {b2}")
        sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Lectura finalizada.")
