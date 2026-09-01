import time
import pandas as pd
import serial

# 1. Establish serial connection to the Arduino port
ser = serial.Serial("/dev/cu.usbmodem11301", 9600)
time.sleep(2)  # Wait for the connection to establish

data_list = []

# 2. Read 10 lines of serial data and parse them
for i in range(10):
  line = ser.readline().decode("utf-8").strip()
  if line:
    print(f"Read raw line: {line}")
    parts = line.split(",")
    # Make sure we have enough columns, then map to the correct indices
    if len(parts) >= 13:
      data_list.append({
          "timestamp": float(parts[0]),
          "temperature": float(parts[10]),  # Index 10 is temperature (~26.26)
          "humidity": float(parts[11]),  # Index 11 is humidity (~40.1)
          "pressure": float(parts[12]),  # Index 12 is pressure (~100.61)
      })

ser.close()

# 3. Store the parsed data into a DataFrame and start the index from 1
df = pd.DataFrame(data_list)
df.index = range(1, len(df) + 1)

# 4. Print the first 5 rows of the DataFrame
print("--- First 5 rows of Arduino sensor data ---")
print(df.head())

# Save the structured data to a CSV file
df.to_csv("arduino_sensor_data.csv", index=False)

# 5. Add 3–5 lines of notes at the bottom of the script
# --- Data Notes ---
# This dataset contains environmental sensor readings (temperature, humidity, and pressure) 
# collected from an Arduino Nano 33 BLE Sense over the serial port.
# It can be used for real-time indoor climate tracking, smart home monitoring, 
# or exploratory data analysis on IoT sensor streams.