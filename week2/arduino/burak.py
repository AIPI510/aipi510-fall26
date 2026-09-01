import serial
import time
import pandas as pd
from pathlib import Path

COLUMNS = [
    "time_ms", "ax_g", "ay_g", "az_g",
    "gx_dps", "gy_dps", "gz_dps",
    "mx_uT", "my_uT", "mz_uT",
    "temp_C", "hum_pct", "press_hPa",
    "roll_deg", "pitch_deg", "heading_deg",
    "mic_rms", "mic_dBFS",
]

ser = serial.Serial("/dev/tty.usbmodem1101", 9600)
time.sleep(2)

raw_lines = []
for i in range(10):
    line = ser.readline().decode("utf-8").strip()
    print(line)
    raw_lines.append(line)

ser.close()

rows = []
for line in raw_lines:
    if not line or line.startswith("time_ms"):
        continue
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != len(COLUMNS):
        continue  # skip first line if its halfway
    rows.append(dict(zip(COLUMNS, parts)))

df = pd.DataFrame(rows)
df = df.apply(pd.to_numeric, errors="coerce")

print(df.head())

csv_path = Path(__file__).with_name("burak_arduino.csv")
df.to_csv(csv_path, index=False)

#Temperature and humidity reading can be pretty useful for a lot of different cases. I for one personally have dreamed of building a automated
#room/cage/habitat for my pet cockatiel, especially now that I live in a galaxy far far away.  
#In the same concept of taking care of a delicate being, I'm sure it would be useful for monitoring the health of plants and senstitive rooms and
#areas like hospital rooms, labs etc. 
#Could also be used to monitor server rooms/data centers where all kinds of evil happens.

