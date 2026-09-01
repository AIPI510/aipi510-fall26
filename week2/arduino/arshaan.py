import serial
import time
import pandas as pd

ser = serial.Serial('/dev/cu.usbmodem14201', 9600)
time.sleep(2)

readings = []

for i in range(10):
    line = ser.readline().decode('utf-8').strip()

    values = line.split(",")

    reading = {
        "temperature_c": float(values[10]),
        "humidity_percent": float(values[11])
    }

    readings.append(reading)

ser.close()

df = pd.DataFrame(readings)

print("First 5 sensor readings:")
print(df.head())


# Notes:
# This project uses the temperature and humidity sensors on an Arduino Nano 33 BLE Sense Rev2.
# The Arduino sends sensor measurements to Python over a USB serial connection.
# The readings are stored in a pandas DataFrame for structured analysis.
# This data could be used to monitor indoor temperature and humidity changes over time.