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
# - Sensor used: Arduino Nano 33 BLE Sense Rev2's onboard IMU (accelerometer/gyroscope/
#   magnetometer) plus environmental sensors (temperature, humidity, pressure, proximity).
# - Each row is one reading pulled from the serial stream, parsed into named columns and timestamped.
# - This data could be used to detect motion or gestures, or to monitor room conditions
#   like temperature and humidity over time.
# - Possible use: building a simple motion-triggered alert or environment logger.
# - Limitation: column labels for the last few values (val1-val4) are best guesses — check
#   the Arduino sketch's Serial.print() order to confirm exact sensor names.