#include <Arduino.h>
#include "Arduino_BMI270_BMM150.h"  // IMU (accel, gyro, mag)
#include <Arduino_HS300x.h>         // ✅ HS3003 on Rev2 (temp & humidity)
#include <Arduino_LPS22HB.h>        // Barometric pressure
#include <PDM.h>                    // PDM microphone

#define BAUD_RATE 9600
static const unsigned long PRINT_INTERVAL_MS = 200; // ~5 Hz
unsigned long lastPrint = 0;

// IMU
float ax, ay, az, gx, gy, gz, mx, my, mz;
float magOffsetX=0, magOffsetY=0, magOffsetZ=0;

// Env
float temperatureC = NAN;
float humidity = NAN;       // optional to print
float pressure_hPa = NAN;

// Mic
volatile bool micReady = false;
volatile size_t micBytes = 0;
const int PDM_BUFFER_SAMPLES = 512;
int16_t micBuffer[PDM_BUFFER_SAMPLES];

void onPDMdata() {
  micBytes = PDM.available();
  if (micBytes > sizeof(micBuffer)) micBytes = sizeof(micBuffer);
  PDM.read(micBuffer, micBytes);
  micReady = true;
}

static inline float rad2deg(float r){ return r * 180.0f / PI; }

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(BAUD_RATE);
  unsigned long t0 = millis();
  while (!Serial && (millis() - t0 < 1500)) { digitalWrite(LED_BUILTIN, (millis()/200)%2); }
  digitalWrite(LED_BUILTIN, LOW);

  // IMU
  if (!IMU.begin()) Serial.println("IMU init failed (continuing)");

  // ✅ HS300x (Rev2 temp/humidity)
  if (!HS300x.begin()) Serial.println("HS300x init failed (continuing)");

  // Pressure
  if (!BARO.begin()) Serial.println("LPS22HB init failed (continuing)");

  // Mic
  PDM.onReceive(onPDMdata);
  if (!PDM.begin(1, 16000)) {
    Serial.println("PDM mic init failed (continuing without mic)");
  } else {
    PDM.setGain(80);
  }

  Serial.println("time_ms, ax_g, ay_g, az_g, gx_dps, gy_dps, gz_dps, mx_uT, my_uT, mz_uT, temp_C, hum_pct, press_hPa, roll_deg, pitch_deg, heading_deg, mic_rms, mic_dBFS");
}

void loop() {
  // Read sensors
  if (IMU.accelerationAvailable()) IMU.readAcceleration(ax, ay, az);
  if (IMU.gyroscopeAvailable())    IMU.readGyroscope(gx, gy, gz);
  if (IMU.magneticFieldAvailable())IMU.readMagneticField(mx, my, mz);

  float roll  = rad2deg(atan2(ay, az));
  float pitch = rad2deg(atan2(-ax, sqrt(ay*ay + az*az)));
  float hx = mx - magOffsetX, hy = my - magOffsetY;
  float heading = rad2deg(atan2(hy, hx)); if (heading < 0) heading += 360.0f;

  temperatureC = HS300x.readTemperature();
  humidity     = HS300x.readHumidity();
  pressure_hPa = BARO.readPressure();

  static float micRMS = 0.0f, micdBFS = -120.0f;
  if (micReady) {
    micReady = false;
    size_t samples = micBytes / 2;
    double sumsq = 0.0;
    for (size_t i=0;i<samples;i++){ float s = micBuffer[i]; sumsq += s*s; }
    if (samples>0){
      micRMS = sqrt(sumsq / samples);
      micdBFS = 20.0f * log10f((micRMS + 1e-6f)/32767.0f);
    }
  }

  if (millis() - lastPrint >= PRINT_INTERVAL_MS) {
    lastPrint = millis();
    Serial.print(lastPrint); Serial.print(", ");
    Serial.print(ax,4);  Serial.print(", "); Serial.print(ay,4);  Serial.print(", "); Serial.print(az,4);  Serial.print(", ");
    Serial.print(gx,2);  Serial.print(", "); Serial.print(gy,2);  Serial.print(", "); Serial.print(gz,2);  Serial.print(", ");
    Serial.print(hx,2);  Serial.print(", "); Serial.print(hy,2);  Serial.print(", "); Serial.print(mz - magOffsetZ,2); Serial.print(", ");
    Serial.print(temperatureC,2);  Serial.print(", ");
    Serial.print(humidity,1);      Serial.print(", ");
    Serial.print(pressure_hPa,2);  Serial.print(", ");
    Serial.print(roll,1);  Serial.print(", "); Serial.print(pitch,1); Serial.print(", "); Serial.print(heading,1); Serial.print(", ");
    Serial.print(micRMS,1); Serial.print(", "); Serial.println(micdBFS,1);
  }
}

