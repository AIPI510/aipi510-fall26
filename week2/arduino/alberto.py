import serial
import time
import pandas as pd

# First we connect to the Arduino
ser = serial.Serial('/dev/tty.usbmodem3101', 9600)

# We wait for the connection to be ready
time.sleep(2)

# These are the sensor columns
columns = [
    "time_ms", "ax_g", "ay_g", "az_g",
    "gx_dps", "gy_dps", "gz_dps",
    "mx_uT", "my_uT", "mz_uT",
    "temp_C", "hum_pct", "press_hPa",
    "roll_deg", "pitch_deg", "heading_deg",
    "mic_rms", "mic_dBFS"
]

# Now we read 10 lines from the sensors
sensorData = []

for i in range(10):
    line = ser.readline().decode("utf-8").strip()
    values = line.split(",")
    sensorData.append(values)

# We close the connection
ser.close()

# Now we store the data in a DataFrame
sensorData = pd.DataFrame(sensorData, columns=columns)

# We save the data to a CSV file
sensorData.to_csv("alberto_sensor_data.csv", index=False)

# Finally, we print the first 5 rows
print(sensorData.head())

# This dataset contains sensor data from the Arduino Nano 33 BLE Sense Rev2.
# It includes movement, temperature, humidity, pressure and microphone data.
# The data could be used to analyze movement and environmental conditions.
# It could also be used to find patterns across the different sensors.