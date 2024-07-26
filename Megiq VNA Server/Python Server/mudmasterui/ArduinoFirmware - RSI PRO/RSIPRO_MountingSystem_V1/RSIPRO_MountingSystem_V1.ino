
const int MotorPinB = 13;     // Motor B pins
const int MotorSpeedPinB = 11;// Motor B speed pin
const int MotorBrakePinB = 8; // Motor B brake pin

const int CW  = HIGH; // Clockwise direction
const int CCW = LOW;  // Counter-clockwise direction

void setup() {


  // Motor B pin initialization
  pinMode(MotorPinB, OUTPUT);
  pinMode(MotorSpeedPinB, OUTPUT);
  pinMode(MotorBrakePinB, OUTPUT);

  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Read the input from serial
    input.trim(); // Remove any leading/trailing whitespace

    // Depending on the input command received from Python
    if (input == "1") {
      // Command to start Motor A clockwise at full speed
      digitalWrite(MotorPinB, HIGH); // Extend Actuator
      analogWrite(MotorSpeedPinB, 255); // Set speed at maximum (255)
      digitalWrite(MotorBrakePinB, LOW); // Release brake if any
      Serial.println("Extended"); // Echo back confirmation
    } else if (input == "2") {
      // Command to start Motor B counterclockwise at full speed
      digitalWrite(MotorPinB, LOW); // Retract Actuator
      analogWrite(MotorSpeedPinB, 255); // Set speed at maximum (255)
      digitalWrite(MotorBrakePinB, LOW); // Release brake if any//
      Serial.println("Retracted"); // Echo back confirmation
    }else if (input == "3") {
      // Command to start Motor B to stop by app
      digitalWrite(MotorBrakePinB, HIGH); // Release brake if any//
    }
    
    delay(100); // Delay for stability
  }
}

