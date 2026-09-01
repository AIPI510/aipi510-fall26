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

# Create a DataFrame from the collected data
df = pd.DataFrame(data)