import time
import board
import busio
from adafruit_pca9685 import PCA9685

def us_to_duty(us):
    return int(us / 20000 * 0xFFFF)

MAX = us_to_duty(2000)
MIN = us_to_duty(1000)
NEUTRAL = us_to_duty(1500)

# Initialize I2C and PCA9685
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50
except Exception as e:
    print(f"❌ Error initializing I2C or PCA9685: {e}")
    exit(1)

# Access channels directly
try:
    channels = [pca.channels[i] for i in range(4)]
except Exception as e:
    print(f"❌ Error accessing channels: {e}")
    exit(1)

print("🔌 Desconecta la batería del ESC.")
input("Presiona ENTER cuando estés listo para calibrar...")

print("🚦 Enviando señal MÁXIMA (2000 µs). AHORA conecta la batería del ESC.")
for ch in channels:
    ch.duty_cycle = MAX
time.sleep(5)

print("📉 Enviando señal MÍNIMA (1000 µs)...")
for ch in channels:
    ch.duty_cycle = MIN
time.sleep(5)

print("⚪ Enviando señal NEUTRA (1500 µs)...")
for ch in channels:
    ch.duty_cycle = NEUTRAL
time.sleep(2)

print("✅ Calibración finalizada. Desconecta la batería y reinicia el ESC si es necesario.")