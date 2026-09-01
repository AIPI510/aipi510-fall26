import serial
import time
import pandas as pd

ser = serial.Serial('/dev/tty.usbmodem11301', 9600)
data = []
time.sleep(2)
for i in range (10):
    line = ser.readline().decode('utf-8').strip()
    print(line)

    values = line.split(",")

    if len(values) == 18:
        data.append(values)
ser.close()


columns = ["time_ms", "ax_g", "ay_g", "az_g","gx_dps", "gy_dps", "gz_dps","mx_uT", "my_uT", "mz_uT","temp_C", "hum_pct", "press_hPa","roll_deg", "pitch_deg", "heading_deg","mic_rms", "mic_dBFS"]

df = pd.DataFrame(data, columns=columns)

df.to_csv("lexielin_sensor_data.csv", index=False)

print(df.head())

# I collected sensor data using the Arduino Nano 33 BLE Sense Rev2.
# The data includes motion, temperature, humidity, pressure, and microphone readings.
# This data could be used to track movement and changes in the environment.