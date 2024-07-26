const int MotorPinA = 12; // for motor A
const int MotorSpeedPinA = 3; // for motor A
const int MotorBrakePinA = 9; // for motor A


const int MotorPinB = 13; // for motor B
const int MotorSpeedPinB = 11;// for motor B
const int MotorBrakePinB = 8;// for motor B

const int CW  = HIGH;
const int CCW = LOW;

void setup() {
  // motor A pin assignment
  pinMode(MotorPinA, OUTPUT);
  pinMode(MotorSpeedPinA, OUTPUT);
  pinMode(MotorBrakePinA, OUTPUT);

  // motor B pin assignment
  pinMode(MotorPinB, OUTPUT);
  pinMode(MotorSpeedPinB, OUTPUT);
  pinMode(MotorBrakePinB, OUTPUT); 


  Serial.begin(9600);//  seial monitor initialized 

}

void loop() {

  //start motor A at maximum speed
  digitalWrite(MotorPinB, CW);// set direction
      Serial.println("Direction CW"); 
  analogWrite(MotorSpeedPinB, 100);// set speed at maximum
      Serial.println("Speed 100");
  delay(5000);// run for 5 seconds

  digitalWrite(MotorPinB, CCW );// set direction
      Serial.println("Direction CCW "); 
  analogWrite(MotorSpeedPinB, 100);// set speed at maximum
      Serial.println("Speed 100");
  delay(5000);// run for 5 seconds



}// loop end

