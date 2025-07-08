from time import sleep
from motor_controller import MotorController
from led_controller import LEDController
from network import DroneReceiver

motors = MotorController()
leds = LEDController([17, 27, 22])
receiver = DroneReceiver()

try:
    while True:
        data = receiver.receive()
        if data:
            y1, x2, y2, b1, b2 = data

            motors.set_motors(throttle=y2, yaw=x2, pitch=y1)

            if b1:
                leds.turn_on()
            else:
                leds.turn_off()

            print(f"Throttle: {y2} | Yaw: {x2} | Pitch: {y1} | B1: {b1} | B2: {b2}")

        sleep(0.1)

except KeyboardInterrupt:
    print("Deteniendo sistema...")
    motors.stop()
    leds.turn_off()
    receiver.close()