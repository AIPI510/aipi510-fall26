import serial
import time
import csv

ser = serial.Serial('/dev/tty.usbmodem3101', 9600)  # Replace with your port, Run in terminal:ls /dev/tty.*
time.sleep(2)  # Wait for connection

output = []

for i in range(10):  # Read 10 lines
    line = ser.readline().decode('utf-8').strip()
    print(line)
    row = [value.strip() for value in line.split(",")]
    output.append(row)

ser.close()


def parse_output_csv(op: list):
    with open("output.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(op)


parse_output_csv(output)
