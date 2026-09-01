import serial
import time
import csv
import pandas as pd

ser = serial.Serial('/dev/tty.usbmodem11301', 9600)
time.sleep(2)

readings = []

columns = ["time_ms", "ax_g", "ay_g", "az_g", "gx_dps", "gy_dps", "gz_dps", "mx_uT", "my_uT", "mz_uT", "temp_C", "hum_pct", "press_hPa", "roll_deg", "pitch_deg", "heading_deg", "mic_rms", "mic_dBFS"]

for i in range(10):
    line = ser.readline().decode('utf-8').strip()
    
    if not line:
        continue
    
    values = line.split(",")
    values = [v.strip() for v in values]
    
    try:
        values = [float(v) for v in values]
    except ValueError:
        print(f"Skipping malformed line: {line}")
        continue
    
    row_dict = dict(zip(columns, values))
    readings.append(row_dict)

ser.close()

print(readings[:2])

df = pd.DataFrame(readings)
print(df.head())

df.to_csv("sensor_data.csv", index=False)

# Notes:
# The dataset here contains IMU, environmental, orientation, and microphone data. This data came from 
# an Arduino sensor board that was connected to the computer port. Some possible things you could do 
# with this data are use it for motion tracking or environmental monitoring.