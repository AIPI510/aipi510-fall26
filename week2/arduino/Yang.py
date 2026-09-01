import serial
import time
import csv
from serial.tools import list_ports


def find_arduino_port():
    ports = list_ports.comports()

    for port in ports:
        description = (port.description or "").lower()

        if (
            "arduino" in description
            or "nano" in description
            or "usb serial" in description
            or "usb" in description
        ):
            return port.device

    if len(ports) > 0:
        return ports[0].device

    raise Exception("No serial device found. Please connect the Arduino.")


arduino_port = find_arduino_port()

print("Using port:", arduino_port)

ser = serial.Serial(arduino_port, 9600, timeout=2)

time.sleep(2)

data = []

for i in range(10):
    line = ser.readline().decode("utf-8").strip()
    print("Raw:", line)

    if line:
        row = {
            "reading_number": i + 1,
            "sensor_data": line
        }

        data.append(row)

ser.close()

csv_file = "Yang_sensor_data.csv"

with open(csv_file, "w", newline="") as file:
    fieldnames = ["reading_number", "sensor_data"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

print("\nFirst 5 rows:")

for row in data[:5]:
    print(row)

print("\nData saved to", csv_file)


# Notes:
# I collected sensor data from the Arduino Nano 33 BLE Sense Rev2.
# The data was read from the Arduino serial output using pyserial.
# I saved the readings into a structured list of dictionaries and then wrote them to a CSV file.
# This type of data could be used to monitor environmental conditions or movement patterns.
# In a larger project, I would collect more rows and analyze trends over time.