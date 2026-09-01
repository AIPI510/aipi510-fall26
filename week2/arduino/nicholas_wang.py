import csv
import serial
import time
ser = serial.Serial('/dev/cu.usbmodem101', 9600)  # Replace with your port
time.sleep(2)  # Wait for connection
lines = []
for i in range(10):  # Read 10 lines
    line = ser.readline().decode('utf-8').strip()
    lines.append(line)
    # print(line)
ser.close()   

# Save to CSV
with open('nw_sensor_output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Wrap each string in a list so it writes as a row, not individual characters
    for line in lines:
        writer.writerow([line])


# print first 5 rows
for line in lines[:5]:
    print(line)
 