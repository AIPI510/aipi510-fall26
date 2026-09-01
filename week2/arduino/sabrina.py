import serial
import time
import pandas as pd

ser = serial.Serial('/dev/tty.usbmodem14201', 9600)
time.sleep(2)  # Wait for connection

columns = ["timestamp_ms", "accelX", "accelY", "accelZ", "gyroX", "gyroY", "gyroZ",
           "magX", "magY", "magZ", "temperature", "humidity", "pressure",
           "proximity", "val1", "val2", "val3", "val4"]

readings = []

for i in range(10):  # Read 10 lines
    line = ser.readline().decode('utf-8').strip()
    print(line)
    if line:
        values = line.split(",")
        values = [v.strip() for v in values]
        if len(values) == len(columns):
            reading = dict(zip(columns, values))
            readings.append(reading)

ser.close()

# Save to DataFrame and CSV
df = pd.DataFrame(readings)
df.to_csv("sabrina_sensor_data.csv", index=False)

print(df.head())




# Notes:
# - Sensor used: Arduino Nano 33 BLE 
# - Collected and cleaned data from the Arduino's built-in sensors, including
#   acceleration and tilt
# - 
# - This data could be used for things like detecting gestures, tracking packages, and more
