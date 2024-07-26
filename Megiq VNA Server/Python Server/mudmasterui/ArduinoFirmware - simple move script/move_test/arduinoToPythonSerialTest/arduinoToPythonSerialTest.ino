int x;

const int MotorPinA = 12; // for motor A
const int MotorSpeedPinA = 3; // for motor A
const int MotorBrakePinA = 9; // for motor A


const int MotorPinB = 13; // for motor B
const int MotorSpeedPinB = 11;// for motor B
const int MotorBrakePinB = 8;// for motor B



void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);

  // motor A pin assignment
  pinMode(MotorPinA, OUTPUT);
  pinMode(MotorSpeedPinA, OUTPUT);
  pinMode(MotorBrakePinA, OUTPUT);

  // motor B pin assignment
  pinMode(MotorPinB, OUTPUT);
  pinMode(MotorSpeedPinB, OUTPUT);
  pinMode(MotorBrakePinB, OUTPUT); 
}

void  loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();

  if (x == 1) {
    digitalWrite(MotorPinB, HIGH);      // Set direction CW
    analogWrite(MotorSpeedPinB, 255); // Set speed at maximum
    Serial.println("extending");      // Print message to serial monitor
    delay(30000);
    analogWrite(MotorSpeedPinB, 0);
  }
  else if (x == 2) {
    digitalWrite(MotorPinB, LOW);     // Set direction CCW
    analogWrite(MotorSpeedPinB, 255); // Set speed at maximum
    Serial.println("retracting");     // Print message to serial monitor
    delay(30000); //leave till max extention which is 210mm
    analogWrite(MotorSpeedPinB, 0);
  }
  else if (x == 3) {
    analogWrite(MotorSpeedPinB, 0);   // Stop motor (set speed to 0)
    Serial.println("Stopping");       // Print message to serial monitor
  }
  else {
    Serial.print(x + 1);  // Print x + 1 if none of the above conditions are met
  }
}