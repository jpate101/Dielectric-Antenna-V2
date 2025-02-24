#include "Adafruit_VL53L1X.h"
#include <Wire.h>
#include <Adafruit_MPU6050.h>  // Include the Adafruit MPU6050 library

// Create instances of the sensors
Adafruit_VL53L1X vl53 = Adafruit_VL53L1X();  // VL53L1X sensor instance
Adafruit_MPU6050 mpu;  // MPU6050 sensor instance

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);

  Serial.println(F("Adafruit VL53L1X sensor demo"));

  // Initialize I2C
  Wire.begin();

  // Initialize the VL53L1X sensor
  if (!vl53.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of VL sensor: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }

  Serial.println(F("VL53L1X sensor OK!"));
  
  Serial.print(F("Sensor ID: 0x"));
  Serial.println(vl53.sensorID(), HEX);

  // Start the ranging process for VL53L1X
  if (!vl53.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }

  Serial.println(F("Ranging started"));

  // Set a longer timing budget to allow for better readings
  vl53.setTimingBudget(500);  // Increase timing budget to 500ms
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53.getTimingBudget());

  // Initialize the MPU6050 sensor
  if (!mpu.begin()) {
    Serial.println("Error initializing MPU6050");
    while (1) delay(10);
  }

  Serial.println("MPU6050 sensor initialized");
}

void loop() {
  int16_t distance;

  // VL53L1X: Read distance
  if (vl53.dataReady()) {
    distance = vl53.distance();

    if (distance == -1) {
      Serial.print(F("Couldn't get distance: "));
      Serial.println(vl53.vl_status);
    } else {
      Serial.print(F("Distance: "));
      Serial.print(distance);
      Serial.println(" mm");
      
      // Calculate the distance to the ground based on pitch and roll
      sensors_event_t aevent;
      mpu.getAccelerometerSensor()->getEvent(&aevent);

      // Extract the acceleration values from the event
      float ax = aevent.acceleration.x;
      float ay = aevent.acceleration.y;
      float az = aevent.acceleration.z;

      // Calculate the pitch and roll angles in degrees
      float pitch = atan2(ay, az) * 180.0 / PI;
      float roll = atan2(ax, az) * 180.0 / PI;

      // Convert pitch and roll to radians
      float pitch_rad = pitch * PI / 180.0;
      float roll_rad = roll * PI / 180.0;

      // Calculate the distance to the ground using trigonometry for both pitch and roll
      // Adjusting for extreme values where pitch and roll approach 180° or -180°
      float distanceToGround = distance * sqrt(pow(cos(pitch_rad), 2) + pow(sin(roll_rad), 2));

      // Output the calculated distance to the ground
      Serial.print("Distance to Ground: ");
      Serial.print(distanceToGround);
      Serial.println(" mm");
    }

    vl53.clearInterrupt();  // Clear interrupt for the next reading
  }

  // MPU6050: Get accelerometer data
  sensors_event_t aevent;
  mpu.getAccelerometerSensor()->getEvent(&aevent);

  // Extract the acceleration values from the event
  float ax = aevent.acceleration.x;
  float ay = aevent.acceleration.y;
  float az = aevent.acceleration.z;

  // Calculate the pitch and roll angles based on accelerometer data
  float pitch = atan2(ay, az) * 180.0 / PI;
  float roll = atan2(ax, az) * 180.0 / PI;

  // Output the pitch and roll angles
  Serial.print("Pitch: ");
  Serial.print(pitch);
  Serial.print(" degrees, ");
  Serial.print("Roll: ");
  Serial.print(roll);
  Serial.println(" degrees");

  // Add some delay to avoid overloading the serial monitor
  delay(3000);  // Short delay before the next reading
}
