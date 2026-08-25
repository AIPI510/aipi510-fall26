import pandas as pd
import serial
import time

cols = ['time_ms', 'ax_g', 'ay_g', 'az_g', 'gx_dps', 'gy_dps', 'gz_dps', 'mx_uT', 'my_uT', 'mz_uT', 'temp_C', 'hum_pct',
        'press_hPa', 'roll_deg', 'pitch_deg', 'heading_deg', 'mic_rms', 'mic_dBFS']

rows = []

ser = serial.Serial('/dev/tty.usbmodem1101', 9600)
time.sleep(2)
for i in range(10):
    line = ser.readline().decode('utf-8').strip().split(', ')
    # Skip malformed lines
    if len(line) != len(cols):
        continue
    rows.append(dict(zip(cols, line)))

ser.close()

df = pd.DataFrame(rows, columns=cols)
df = df.apply(pd.to_numeric, errors='coerce')

print(df.head(5))

# AI Disclosure: ChatGPT was used on 9/2/2025 to assist in creating the Pandas code to create the columns and rows
# The data could be used for a variety of things. It seems like it tracks movement and the ambient temperature and other various things
# It could be used to track temperature over time or used as a gyroscope to track movement
