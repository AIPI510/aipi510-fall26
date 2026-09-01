import serial
import time
import pandas as pd

ser = serial.Serial('/dev/tty.usbmodem11301', 9600)
time.sleep(2)
data = []
features = 18
trials = 10

for i in range(trials):
    # gets data
    line = ser.readline().decode('utf-8').strip()
    # splits data between commas
    parts = line.split(',')
    # makes data into float values
    row_values = [float(val) for val in parts]
    # adds data into data list 
    data.append(row_values)
ser.close()
cols = ["time_ms", "ax_g", "ay_g", "az_g", "gx_dps", "gy_dps", "gz_dps", "mx_uT", "my_uT", "mz_uT", "temp_C", "hum_pct", "press_hPa", "roll_deg", "pitch_deg", "heading_deg", "mic_rms", "mic_dBFS"]

df = pd.DataFrame(data, columns=cols)
print(df)

""" This code can be used to record Arduino data.
    It takes input from the Arduino and records it in the dataframe df.
    It them prints out the df to the user.
"""