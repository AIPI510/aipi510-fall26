import serial
import time
import pandas as pd

ser = serial.Serial('/dev/tty.usbmodem1101', 9600)

time.sleep(2)

data = []

for i in range(10):
    line = ser.readline().decode('utf-8').strip()
    values = line.split(', ')
    data.append(values)

ser.close()

df = pd.DataFrame(data, columns=["time_ms", "ax_g", "ay_g", "az_g", "gx_dps", "gy_dps", "gz_dps", "mx_uT", "my_uT", "mz_uT", "temp_C", "hum_pct", "press_hPa", "roll_deg", "pitch_deg", "heading_deg", "mic_rms", "mic_dBFS"])

print(df.head())

df.to_csv('../data/arduino_data.csv', index=False)

# The Arduino Nano 33 BLE Sense Rev2 collects multiple sensor measurements.
# The data includes motion and environmental sensor readings.
# This data could be used to analyze changes in sensor measurements over time.
# It could also be used to identify patterns in movement or environmental conditions.