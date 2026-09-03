import serial
import time
import pandas as pd

# 1. Connect to the Arduino through serial
ser = serial.Serial('/dev/cu.usbmodem1101', 9600)
time.sleep(2)

# List to store sensor readings in a structured format (dicts)
structured_data = []

print("Reading and parsing serial sensor output...")

for i in range(10):
    # 2. Read serial sensor output
    line = ser.readline().decode('utf-8').strip()
    
    # 3. Parse the serial output (assumes comma-separated "sensor_id,value" or simple float values)
    if line:
        try:
            # Check if output is comma-separated (e.g., "1,23.5") or a single value (e.g., "23.5")
            if ',' in line:
                sensor_id, value = line.split(',')
                reading = {"reading_id": i + 1, "sensor_id": sensor_id.strip(), "value": float(value.strip())}
            else:
                reading = {"reading_id": i + 1, "value": float(line)}
            
            # 4. Store sensor readings in a structured format (dictionary)
            structured_data.append(reading)
        except ValueError:
            # Fallback if output contains non-numeric header text
            structured_data.append({"reading_id": i + 1, "value": line})

ser.close()

# 5. Store collected data in a DataFrame and save to CSV
df = pd.DataFrame(structured_data)
df.to_csv("arduino_sensor_data.csv", index=False)

# 6. Display collected data
print("\n--- Collected Arduino Sensor Data ---")
print(df)
print("Data successfully saved to 'arduino_sensor_data.csv'.\n")

# Display at least 3 lines of notes
print("--- Notes on Arduino Data Collection ---")
print("1. This script establishes a 9600-baud serial connection with the Arduino microcontroller to stream live telemetry.")
print("2. Raw incoming byte strings are decoded to UTF-8, stripped of whitespace, parsed into key-value structures, and stored in a Pandas DataFrame.")
print("3. The structured dataset is automatically exported to a local CSV file to enable downstream statistical analysis and visualization.")