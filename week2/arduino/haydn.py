import serial 
import time 
import csv
import os

ser = serial.Serial('/dev/tty.usbmodem1101', 9600) # Add the port time.sleep(2)

# Check if the Ouput CSV Exists 
file_exists = os.path.isfile('data.csv')

# Create the Lines List 
line_list = []

for i in range(10): # read 10 lines 
    line = ser.readline().decode('utf-8').strip()
    print(line)
    line_list.append(line)

    # add the line to the list
    with open('data.csv', 'a', newline='') as f:
        # open the CSV file
        writer = csv.writer(f) # create the CSV writer

        if not file_exists: writer.writerow(['reading']) # header, only written once

        for line in line_list:
            writer.writerow([line])
            ser.close()

for i in range(5):
    print(line_list[i]) # print the first 5 lines (Step 7)

# I used the accelerometer sensor.
# One project I would use this data for is to track motion and orientation of a drone.
# This way you can monitor human flight responses by logging the data.
