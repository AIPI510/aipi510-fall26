# STATION 3: Collect Data Using Arduino Nano 33 BLE Sense Rev2

## Objective:
Collect sensor data (e.g., temperature, light, movement) and save it to a CSV.

## Setup:
Your Arduino should already be connected and flashed with the appropriate sketch (we will provide an example sketch that streams serial sensor data).
Use Python with pyserial to read the serial output.

## Step-by-step:
1. Clone the class repo and branch off of the branch week2 (only do once, at your first station) 
2. Create a new branch yourname-week2 (only do once, at your first station)
3. Create a new file named yourname.py in arduino/ 
4. Install pyserial if needed
5. Use the following Python boilerplate to collect serial data:

```
import serial
import time
ser = serial.Serial('/dev/tty.usbmodemXXXX', 9600)  # Replace with your port
time.sleep(2)  # Wait for connection
for i in range(10):  # Read 10 lines
    line = ser.readline().decode('utf-8').strip()
    print(line)
ser.close()
```

6. Modify your script to:
- Parse the output into a structured format (dict or list)
- Save it to a CSV or DataFrame


7. Print the first 5 rows.
8. Add 3–5 lines of notes at the bottom of the script describing what sensor you used and what you’d do with the data.
9. Commit
