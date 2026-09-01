import serial
import time
import pandas as pd

ser = serial.Serial('/dev/tty.usbmodem101', 9600)

time.sleep(2)

for i in range(10):
    line = ser.readline().decode('utf-8').strip()
    line_list = line.split(',')
    print(line_list)

# convert to lists and then to a dataframe
df = pd.DataFrame([line.split(',') for line in ser.readlines()], columns=[
    'time_ms',
    'ax_g',
    'ay_g',
    'az_g',
    'gx_dps',
    'gy_dps',
    'gz_dps',
    'mx_uT',
    'my_uT',
    'mz_uT',
    'temp_C',
    'hum_pct',
    'press_hPa',
    'roll_deg',
    'pitch_deg',
    'heading_deg',
    'mic_rms',
    'mic_dBFS'
])
print(df.head())

ser.close()

'''
The values of the data from the Arduino is a list of time, motion, temperature, pressure, 
orientation, and sound. This data can be used to analyze the environment and conditions of the sensor.
It could also be used to train a model to predict certain conditions given certain inputs such as
the movements of the sensor.
'''