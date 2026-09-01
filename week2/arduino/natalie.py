import serial
import time
import pandas as pd

ser = serial.Serial("/dev/tty.usbmodem101", 9600)
time.sleep(2)

data_list = []
for i in range(10):
    line = ser.readline().decode("utf-8").strip()
    data_list.append(line)
    print(line)
ser.close()


df = pd.DataFrame(data_list, columns=['Sensor_Value'])
print(df.head())


# Save the DataFrame to a CSV file pulling arduino data

