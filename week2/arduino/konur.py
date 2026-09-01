import serial
import time
import pandas as pd


COLUMNS = [
    "timestamp",
    "sensor_1",
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_5",
    "sensor_6",
    "sensor_7",
    "sensor_8",
    "sensor_9",
    "sensor_10",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_14",
    "sensor_15",
    "sensor_16",
    "sensor_17",
]


def parse_line(line):
    values = line.split(",")

    # Remove whitespace around each value
    values = [value.strip() for value in values]

    if len(values) != len(COLUMNS):
        print(f"Skipping malformed line: {line}")
        return None

    try:
        # First value appears to be a timestamp/integer
        values[0] = int(values[0])

        # Remaining sensor readings are floats
        values[1:] = [float(value) for value in values[1:]]

    except ValueError:
        print(f"Could not parse line: {line}")
        return None

    return dict(zip(COLUMNS, values))


ser = serial.Serial("/dev/tty.usbmodem11101", 9600, timeout=2)

time.sleep(2)

records = []

for i in range(10):
    line = ser.readline().decode("utf-8").strip()

    if line:
        data = parse_line(line)

        if data is not None:
            records.append(data)

ser.close()

df = pd.DataFrame(records)
print(df.head())

# Hardware: Arduino Nano 33 BLE Sense Rev2 with built-in motion and environmental sensors.
# The sensor data is read over USB serial and stored in a pandas DataFrame.
# This data could be used for visualization, motion/environment analysis, or as input to a machine-learning model.