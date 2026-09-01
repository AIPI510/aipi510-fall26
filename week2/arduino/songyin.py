import serial
import time
import pandas as pd

# Connect to the Arduino serial port
# Replace COM4 with the actual port later
ser = serial.Serial("COM4", 9600)

# Wait for the connection
time.sleep(2)

# Create an empty list to store sensor readings
data = []

# Read 10 lines of sensor data
for i in range(10):
    line = ser.readline().decode("utf-8").strip()
    print(line)

    # Store each reading in a dictionary
    data.append({
        "sensor_value": line
    })

# Close the serial connection
ser.close()

# Convert the list into a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("arduino_data.csv", index=False)

# Print the first 5 rows
print(df.head())

# Notes:
# This script collects sensor data from an Arduino Nano 33 BLE Sense Rev2.
# The readings are received through the serial port.
# The data is stored in a pandas DataFrame and saved to a CSV file.
# The data could be used for sensor monitoring, analysis, or visualization.