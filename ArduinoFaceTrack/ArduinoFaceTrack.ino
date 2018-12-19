#include <Servo.h>

Servo myServo;
int servoPos = 90;
int editAmount = 10;
float factor = 1.5f;
bool autoAmount = true;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
  myServo.attach(9);
  myServo.write(servoPos);
}

void loop() {
  /*if (Serial.available() > 0)
  {
    servoPos = Serial.readString().toInt();
    if (servoPos != NULL)
    {
      myServo.write(servoPos);
    }*/
  if (Serial.available())//  > 0 && myServo.read() == servoPos
  {
    String incomingData = Serial.readString();
    if (autoAmount==true){
      editAmount = (incomingData[2] - '0')*factor;
      Serial.println(editAmount);
    }
    //Serial.print(incomingData);
    
    if (incomingData[0] == '-' && servoPos >= 2+editAmount)
    {
      servoPos-=editAmount;
    }
    else if (incomingData[0] == '+' && servoPos <= 180-editAmount)
    {
      servoPos+=editAmount;
    }
    
    if (servoPos >= 2 && servoPos <= 180 && servoPos != NULL)
    {
      myServo.write(servoPos);
    }
    
  }
  //Serial.println(servoPos);
}
