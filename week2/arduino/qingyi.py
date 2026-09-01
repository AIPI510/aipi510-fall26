"""Collect multi-sensor readings from a Nano 33 BLE Sense Rev2 into a DataFrame."""

import sys
import time

import pandas as pd
import serial
from serial.tools import list_ports

SERIAL_PORT = "COM4"
BAUD_RATE = 9600
N_READINGS = 10
OUTPUT_CSV = "arduino_readings.csv"

# One name per value printed by the sketch, in the same order.
# Verify the ch* placeholders against the Serial.print order in your .ino.
COLUMNS = [
    "millis",
    "accel_x_g", "accel_y_g", "accel_z_g",          # BMI270
    "gyro_x_dps", "gyro_y_dps", "gyro_z_dps",       # BMI270
    "mag_x_ut", "mag_y_ut", "mag_z_ut",             # BMM150
    "temperature_c",                                # HS3003
    "humidity_pct",                                 # HS3003
    "pressure_kpa",                                 # LPS22HB
    "roll_deg", "pitch_deg", "yaw_deg",
    "mic_rms", "mic_dbfs",                          # MP34DT06JTR
]

INTEGER_COLUMNS = ["millis", "mag_x_ut", "mag_y_ut", "mag_z_ut"]


def list_available_ports() -> None:
    """Print detected serial ports so you can find the right one."""
    ports = list_ports.comports()
    if not ports:
        print("No serial ports detected. Is the board plugged in?")
    for p in ports:
        print(f"  {p.device} - {p.description}")


def parse_line(raw: str, columns: list[str]) -> dict | None:
    """Turn one serial line into a dict. Returns None if the line is unusable."""
    raw = raw.strip()
    if not raw:
        return None

    values = [v.strip() for v in raw.split(",")]
    if len(values) != len(columns):
        print(f"  skipped (expected {len(columns)} values, got {len(values)}): {raw!r}")
        return None

    return {
        col: pd.to_numeric(val, errors="coerce")
        for col, val in zip(columns, values)
    }


def collect_readings() -> list[dict]:
    """Open the port, read N_READINGS lines, parse each into a dict."""
    records = []
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
    except serial.SerialException as exc:
        print(f"Could not open {SERIAL_PORT}: {exc}\n\nAvailable ports:")
        list_available_ports()
        sys.exit(1)

    with ser:
        time.sleep(2)              # board resets when the port opens; wait it out
        ser.reset_input_buffer()   # drop partial lines buffered during the reset

        for i in range(N_READINGS):
            raw = ser.readline().decode("utf-8", errors="replace").strip()
            print(f"[{i + 1}/{N_READINGS}] {raw!r}")

            record = parse_line(raw, COLUMNS)
            if record is None:
                continue

            record["reading_num"] = i + 1
            records.append(record)

    return records


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop failed parses, fix dtypes, add a derived column."""
    if df.empty:
        return df

    value_cols = [c for c in df.columns if c != "reading_num"]

    # a row where every sensor value failed to convert is not usable
    df = df.dropna(subset=value_cols, how="all")
    df = df.drop_duplicates()

    # counters and raw integer counts are not continuous measurements
    for col in INTEGER_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("Int64")

    # total acceleration: sits near 1.0 g whenever the board is at rest,
    # regardless of how it is tilted
    accel = ["accel_x_g", "accel_y_g", "accel_z_g"]
    if all(c in df.columns for c in accel):
        df["accel_mag_g"] = (df[accel] ** 2).sum(axis=1) ** 0.5

    ordered = ["reading_num"] + value_cols + ["accel_mag_g"]
    return df[[c for c in ordered if c in df.columns]].reset_index(drop=True)


def main() -> pd.DataFrame:
    readings = collect_readings()

    if not readings:
        sys.exit("No readings parsed. Check COLUMNS matches your sketch output.")

    df = clean(pd.DataFrame(readings))

    print("\nFirst 5 rows:")
    print(df.head(5).to_string())
    print(f"\nShape: {df.shape}")

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved to {OUTPUT_CSV}")

    return df


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# NOTES ON THE DATA
#
# Readings come from an Arduino Nano 33 BLE Sense Rev2, which prints all of its
# onboard sensors as one comma-separated line every ~215 ms at 9600 baud. Each
# row holds 18 channels: a millis() timestamp, accelerometer and gyroscope from
# the BMI270 IMU, magnetometer from the BMM150, temperature and humidity from
# the HS3003, barometric pressure from the LPS22HB, roll/pitch/yaw derived on
# the board, and the microphone's RMS level in raw counts and dBFS.
#
# Accelerometer magnitude holds at 0.989 g across every sample, so the board
# was stationary but tilted, and the gyroscope columns are measuring the sensor
# noise floor rather than rotation. Two artifacts matter: temperature climbed
# from 27.0 to 29.5 C across runs while humidity fell, which is the board self-
# heating rather than the room changing, and yaw sits pinned near 270 degrees
# because the magnetometer is uncalibrated and indoors. millis() resets on
# every power cycle, so it is only comparable within a single run.
#
# Useful for characterising each sensor's noise floor as a baseline for anomaly
# detection, for detecting motion or orientation change once the board is moved,
# or for quantifying the self-heating offset so the temperature channel could be
# corrected for ambient logging.
# ---------------------------------------------------------------------------