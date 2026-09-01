

import serial

import time
import pandas as pd

ser = serial.Serial('/dev/tty.usbmodem11301', 9600)

time.sleep(2)

measurements = []
for _ in range(10):
    line = ser.readline().decode('utf-8').strip()
    measurements.append(line.split(', '))
ser.close()

df = pd.DataFrame(
    measurements,
    columns="time_ms, ax_g, ay_g, az_g, gx_dps, gy_dps, gz_dps, mx_uT, my_uT, mz_uT, temp_C, hum_pct, press_hPa, roll_deg, pitch_deg, heading_deg, mic_rms, mic_dBFS".split(", ")
)
print(df.head())

"""
arduino code
is in
.ino file
"""
