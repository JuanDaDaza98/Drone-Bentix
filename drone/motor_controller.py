import board
import busio
from adafruit_pca9685 import PCA9685
from time import sleep

class MotorController:
    def __init__(self, i2c_freq=50):
        """Initialize the motor controller with PCA9685."""
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.pca = PCA9685(i2c)
            self.pca.frequency = i2c_freq
        except Exception as e:
            raise RuntimeError(f"Error initializing I2C or PCA9685: {e}")

    def us_to_duty(self, microseconds: int) -> int:
        """Converts microseconds to a 16-bit duty cycle value."""
        return int(microseconds / 20000 * 0xFFFF)

    def map_joystick_value_to_us(self, value: int) -> int:
        """Maps joystick value (0-255) to ESC microsecond pulse (1150-1850)."""
        center = 128
        if value < center:
            return int(1150 + (value / 127) * (1500 - 1150))
        else:
            return int(1500 + ((value - center) / 127) * (1850 - 1500))

    def clip(self, value: int, min_val: int = 0, max_val: int = 255) -> int:
        """Ensures the value stays within the 0-255 range."""
        return max(min_val, min(max_val, value))

    def clip_deadzone(self, value: int, deadzone: int = 3) -> int:
        if abs(value - 128) <= deadzone:
            return 128
        return value
    
    def set_motors(self, throttle: int, yaw: int, pitch: int) -> None:
        """
        Controla 4 motores:
        - M1 y M2: propulsión vertical (ascenso/descenso), controlados por throttle (y2)
        - M3 y M4: propulsión horizontal y rotación, controlados por pitch (y1) y yaw (x2)
        """
        throttle = self.clip_deadzone(self.clip(throttle))
        yaw = self.clip_deadzone(self.clip(yaw))
        pitch = self.clip_deadzone(self.clip(pitch))

        # Motores M1 y M2 (verticales, ascenso/descenso)
        m1_us = self.map_joystick_value_to_us(self.clip(throttle))
        m2_us = m1_us  # mismo valor

        # Motores M3 y M4 (horizontales, avance y giro)
        # Avance/retroceso = pitch
        # Giro = yaw, aplicado en sentidos opuestos
        base = pitch
        rotation = yaw - 128                  # centrado en 0
        m3_input = self.clip(base + rotation)
        m4_input = self.clip(base - rotation)

        m3_us = self.map_joystick_value_to_us(m3_input)
        m4_us = self.map_joystick_value_to_us(m4_input)

        # Enviar señales PWM
        self.pca.channels[0].duty_cycle = self.us_to_duty(m1_us)
        self.pca.channels[2].duty_cycle = self.us_to_duty(m2_us)
        self.pca.channels[1].duty_cycle = self.us_to_duty(m3_us)
        self.pca.channels[3].duty_cycle = self.us_to_duty(m4_us)

#        print(f"rotacion: {m3_input}, {m4_input} ------ giro de: {rotation}")


    def stop(self):
        """Sends neutral pulse (1500 µs) to all motors (stops them)."""
        neutral = self.us_to_duty(1500)
        for ch in self.pca.channels[:4]:
            ch.duty_cycle = neutral
        print("Todos los motores detenidos (1500 μs).")
