import serial
import time

ser = serial.Serial('/dev/tty.usbmodem1101',9600)
time.sleep(2)

headers = [
    'time_ms', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7',
    'col8', 'col9', 'col10', 'col11', 'col12', 'col13', 'col14',
    'col15', 'col16', 'col17', 'col18'
]

data = []

for i in range(10):
    line = ser.readline().decode('utf-8').strip()
    print(line)
ser.close()

print("\nStructured data:")
for row in data:
    print(row)