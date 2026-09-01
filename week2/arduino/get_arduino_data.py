import serial
import time
ser = serial.Serial('COM4', 9600)  # Replace with your port, Run in terminal:ls /dev/tty.*
time.sleep(2)  # Wait for connection
for i in range(10):  # Read 10 lines
    line = ser.readline().decode('utf-8').strip()
    print(line)
ser.close()
