#include "Adafruit_VL53L1X.h"
#include <Wire.h>
#include <Adafruit_MPU6050.h>  // Include the Adafruit MPU6050 library

// Motor pin definitions
const int MotorPinB = 13;     // Motor B pins
const int MotorSpeedPinB = 11; // Motor B speed pin
const int MotorBrakePinB = 8;  // Motor B brake pin

const int CW = HIGH;  // Clockwise direction
const int CCW = LOW;  // Counter-clockwise direction

// Create instances of the sensors
Adafruit_VL53L1X vl53 = Adafruit_VL53L1X();  // VL53L1X sensor instance
Adafruit_MPU6050 mpu;  // MPU6050 sensor instance

// Function to initialize VL53L1X with timeout
bool initializeVL53L1X(unsigned long timeout) {
  unsigned long startMillis = millis();
  while (!vl53.begin(0x29, &Wire)) {
    if (millis() - startMillis >= timeout) {
      return false;  // Timeout reached, return failure
    }
    delay(10);  // Small delay to avoid locking the CPU
  }
  return true;  // Successfully initialized
}

// Function to initialize MPU6050 with timeout
bool initializeMPU(unsigned long timeout) {
  unsigned long startMillis = millis();
  while (!mpu.begin()) {
    if (millis() - startMillis >= timeout) {
      return false;  // Timeout reached, return failure
    }
    delay(10);  // Small delay to avoid locking the CPU
  }
  return true;  // Successfully initialized
}

void setup() {
  // Motor pin initialization
  pinMode(MotorPinB, OUTPUT);
  pinMode(MotorSpeedPinB, OUTPUT);
  pinMode(MotorBrakePinB, OUTPUT);

  Serial.begin(9600); // Initialize serial communication
  while (!Serial) delay(10);  // Wait for serial monitor

  // Initialize I2C
  Wire.begin();

  // Initialize the VL53L1X sensor with a 5-second timeout
  if (!initializeVL53L1X(5000)) {
    //Serial.println(F("Error: VL53L1X initialization timed out."));
    while (1) delay(10);  // Halt the program after timeout (or handle as needed)
  }

  // Start the ranging process for VL53L1X
  if (!vl53.startRanging()) {
    //Serial.print(F("Couldn't start ranging: "));
    //Serial.println(vl53.vl_status);
    while (1) delay(10);
  }

  // Initialize the MPU6050 sensor with a 5-second timeout
  if (!initializeMPU(5000)) {
    //Serial.println("Error: MPU6050 initialization timed out. Continuing...");
  } else {
    //Serial.println("MPU6050 sensor initialized successfully.");
  }
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Read the input from serial
    input.trim(); // Remove any leading/trailing whitespace

    // Depending on the input command received from Python
    if (input == "1") {
      // Command for RSI PRO Extend
      digitalWrite(MotorPinB, HIGH); // Extend Actuator
      analogWrite(MotorSpeedPinB, 255); // Set speed at maximum (255)
      digitalWrite(MotorBrakePinB, LOW); // Release brake if any
      Serial.println("Extended"); // Echo back confirmation
    } else if (input == "2") {
      // Command for RSI PRO Retract
      digitalWrite(MotorPinB, LOW); // Retract Actuator
      analogWrite(MotorSpeedPinB, 255); // Set speed at maximum (255)
      digitalWrite(MotorBrakePinB, LOW); // Release brake if any
      Serial.println("Retracted"); // Echo back confirmation
    } else if (input == "3") {
      // Command for RSI PRO Stop
      digitalWrite(MotorBrakePinB, HIGH); // Apply brake
      Serial.println("Stopped"); // Echo back confirmation
    } else if (input == "4") {
      // Command to check connection
      Serial.println("check success"); // Echo back confirmation
    } else if (input == "5") {
    // Command to get the distance to the ground
      int16_t distance = vl53.distance();
      if (distance == -1) {
          // Check if the VL53L1X is working
          Serial.println("ERROR: Couldn't get distance from VL53L1X.");
      } else {
          // Calculate the distance to the ground based on pitch and roll
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

        // Step 1: Adjust for pitch first (keep roll the same)
        float pitchAdjusted = pitch_rad;  // Use the raw pitch value or adjust it
        float rollAdjusted = roll_rad;    // Keep the original roll for this calculation

        // Step 2: Adjust for roll separately (keep pitch the same)
        rollAdjusted = roll_rad;  // Use the raw roll value or adjust it
        pitchAdjusted = pitch_rad; // Keep the original pitch for this calculation

        // Calculate the distance using the adjusted roll
        float distanceToGround = distance * cos(rollAdjusted) * cos(pitchAdjusted);

        // Now, you can compare both distances and observe how each angle impacts the result.
        Serial.print("Distance to Ground: ");
        Serial.println(distanceToGround);
        }
    }
    delay(100); // Delay for stability
  }
}

