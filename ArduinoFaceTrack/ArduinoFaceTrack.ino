#include <Servo.h>

Servo myServo;
int servoPos = 90;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
}

void loop() {
  if (Serial.available() > 0)
  {
    String incomingData = Serial.readString();
    if (incomingData[0] == '+')
    {
      servoPos-=10;
    }
    else if (incomingData[0] == '-')
    {
      servoPos+=10;
    }
    else if (incomingData[0] == 'z')
    {
      servoPos += 0;
    }
  }
  if (servoPos > 45 && servoPos < 135)
  {
    myServo.write(servoPos);
  }
}
