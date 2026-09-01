import serial
import time
import pandas as pd
import csv


def getArduionoData():
    data = []
    ser = serial.Serial('/dev/tty.usbmodem2101', 9600)  # Replace with your port
    time.sleep(2)  # Wait for connection
    for i in range(10):  # Read 10 lines
        line = ser.readline().decode('utf-8').strip()
        data.append(line)
        # print(line)
    ser.close()

    #from flas_sensor_print
    header = ["time_ms, ax_g, ay_g, az_g, gx_dps, gy_dps, gz_dps, mx_uT, my_uT, mz_uT, temp_C, hum_pct, press_hPa, roll_deg, pitch_deg, heading_deg, mic_rms, mic_dBFS"]


    # save to CSV
    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)  # Writes all rows at once
    
    df =  pd.DataFrame(data, columns = header)
    print(df.head())




if __name__ == "__main__":
    getArduionoData()

# The scrip reads, the collumns are  time_ms, ax_g, ay_g, az_g, gx_dps, gy_dps, gz_dps, mx_uT, my_uT, mz_uT, temp_C, hum_pct, press_hPa, roll_deg, pitch_deg, heading_deg, mic_rms, mic_dBFS
# so it reads:
#  time series
# IMU - internal measurement unit (Acceleromentr, Gyroscpoe, Magnetometer)
# ENV - temperature, humidty, presure
# MIC - microphone data