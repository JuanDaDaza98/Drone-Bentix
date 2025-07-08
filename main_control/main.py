from time import sleep
from joystick_reader import JoystickReader
from network_sender import DroneSender

joystick = JoystickReader()
sender = DroneSender()

try:
    while True:
        y1, x2, y2, b1, b2 = joystick.read()
        data = [y1, x2, y2, b1, b2]
        sender.send(data)
        sleep(0.1)

except KeyboardInterrupt:
    print("Finalizando controlador...")