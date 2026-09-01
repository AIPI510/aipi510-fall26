import serial
import time
import json
import pandas as pd

ser = serial.Serial('/dev/tty.usbmodem1101', 9600)

time.sleep(2)

headers = [
    "time_ms",
    "ax_g", "ay_g", "az_g",
    "gx_dps", "gy_dps", "gz_dps",
    "mx_uT", "my_uT", "mz_uT",
    "temp_C", "hum_pct", "press_hPa",
    "roll_deg", "pitch_deg", "heading_deg",
    "mic_rms", "mic_dBFS"
]

data = []

for i in range(10):
    line = ser.readline().decode('utf-8').strip()
    values = line.split(",")

    # Only use complete rows
    if len(values) == len(headers):
        values = [float(value.strip()) for value in values]

        row = dict(zip(headers, values))

        data.append(row)

data = pd.DataFrame(data, columns=headers)

data.to_csv("dd.csv", index=False)

ser.close()

print(data.head())

# This script collects data from sensors that measure motion, orientation, environmental information on conditions and sound.
# The collected data could be used to track movement around the sensor for a speific period of time. Like a patient leaving their hospital bed or how often a restaurant fridge is opened.