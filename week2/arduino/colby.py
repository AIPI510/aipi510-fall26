import serial
import time
import pandas as pd

data = []

ser = serial.Serial('COM4', 9600)
time.sleep(2)

for i in range(10):
    line = ser.readline().decode('utf-8').strip()
    if line:
        parts = line.split(',')
        
        selected_row = {
            'temp_C': float(parts[10]),
            'hum_pct': float(parts[11])
        }
        data.append(selected_row)
    print(line)
ser.close()

df = pd.DataFrame(data)
print(df.head())

'''
This script uses the temperature and humidity sensors on the Arduino to collect temperature and humidity data.
The data is stored in a pandas DataFrame, with each row containing the temperature in Celsius and the humidity percentage.
The data can be used to examine weather conditions in a given area, perhaps for a later visualization.
'''