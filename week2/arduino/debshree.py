import serial
import time
ser = serial.Serial('/dev/cu.usbmodem1101',9600)
time.sleep(2)
for i in range(10):
    line = ser.readline().decode('utf-8').strip()
    print(line)



ser.close()

'''This code helps us to read the data from arduino sensors'''
