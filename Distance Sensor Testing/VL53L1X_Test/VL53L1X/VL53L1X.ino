#include "Adafruit_VL53L1X.h"

Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(); // No need to specify IRQ_PIN and XSHUT_PIN

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);

  Serial.println(F("Adafruit VL53L1X sensor demo"));

  Wire.begin();
  
  if (!vl53.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of VL sensor: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }

  Serial.println(F("VL53L1X sensor OK!"));
  
  Serial.print(F("Sensor ID: 0x"));
  Serial.println(vl53.sensorID(), HEX);

  if (!vl53.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }

  Serial.println(F("Ranging started"));

  vl53.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53.getTimingBudget());
}

void loop() {
  int16_t distance;

  if (vl53.dataReady()) {
    distance = vl53.distance();
    
    if (distance == -1) {
      Serial.print(F("Couldn't get distance: "));
      Serial.println(vl53.vl_status);
    } else {
      Serial.print(F("Distance: "));
      Serial.print(distance);
      Serial.println(" mm");
    }

    vl53.clearInterrupt();
  }

  delay(500);  // Short delay before the next reading
}