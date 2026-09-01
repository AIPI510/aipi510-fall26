
import serial
import time
import pandas as pd

# Connect to Arduino
ser = serial.Serial('/dev/tty.usbmodem1101', 9600)
time.sleep(2)

records = []

# Read 10 lines of sensor data
for i in range(10):
    line = ser.readline().decode('utf-8').strip()
    print(line)

    # Parse the comma-separated sensor data
    values = [value.strip() for value in line.split(",")]

    if len(values) == 18:
        records.append(values)

ser.close()

# Store the data in a DataFrame
columns = [
    "timestamp",
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_5",
    "sensor_6",
    "sensor_7",
    "sensor_8",
    "sensor_9",
    "sensor_10",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_14",
    "sensor_15",
    "sensor_16",
    "sensor_17",
    "sensor_18"
]

df = pd.DataFrame(records, columns=columns)

# Print the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Save the data to a CSV file
df.to_csv("week2/arduino/arduino_data.csv", index=False)

# Notes:
# This data was collected using an Arduino Nano 33 BLE Sense Rev2.
# The Arduino streams 18 sensor values over a serial connection.
# The data is parsed into a structured Pandas DataFrame.
# The data is saved to a CSV file for further analysis.
# The data could be used to analyze environmental and motion measurements.

