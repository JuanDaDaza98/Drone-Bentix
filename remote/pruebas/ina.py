import board
import busio
import adafruit_ina260

try:
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_ina260.INA260(i2c)
    
    print("Voltaje:", sensor.voltage, "V")
    print("Corriente:", sensor.current, "mA")
    print("Potencia:", sensor.power, "mW")
except Exception as e:
    print("Error:", e)
