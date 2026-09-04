import serial
import time
import csv
import os
ser = serial.Serial('/dev/tty.usbmodem1101', 9600)  # Replace 'XXXX' with your Arduino's port
time.sleep(2)  # Wait for the serial connection to initialize

# Column names, in order - matches the header line the Arduino sketch prints
# (time_ms, ax_g, ay_g, az_g, gx_dps, gy_dps, gz_dps, mx_uT, my_uT, mz_uT,
#  temp_C, hum_pct, press_hPa, roll_deg, pitch_deg, heading_deg, mic_rms, mic_dBFS)
columns = ["time_ms", "ax_g", "ay_g", "az_g", "gx_dps", "gy_dps", "gz_dps",
           "mx_uT", "my_uT", "mz_uT", "temp_C", "hum_pct", "press_hPa",
           "roll_deg", "pitch_deg", "heading_deg", "mic_rms", "mic_dBFS"]

data = []  # will hold one dict per sensor reading
for i in range(10):
    line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
    print(line)  # Print the line to the console
    values = line.split(',')  # split the comma-separated string into a list of value strings
    row = dict(zip(columns, values))  # pair each column name with its matching value -> a dict
    data.append(row)  # add this reading's dict to our list
ser.close()  # Close the serial connection

# Write the collected readings to a CSV file in this same folder (arduino/),
# regardless of what directory the script is run from.
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "sensor_data.csv")

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()   # write the column names as the first row
    writer.writerows(data)  # write one row per reading

print(f"Wrote {len(data)} rows to {csv_path}")

for row in data[:5]:  # print just the first 5 structured readings to check the result
    print(row)
