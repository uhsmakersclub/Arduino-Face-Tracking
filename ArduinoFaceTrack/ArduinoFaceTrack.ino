#include <Servo.h>

Servo xServo;
Servo yServo;
int xServoPos = 90;
int yServoPos = 90;
int xEditAmount = 10;
int yEditAmount = 10;
float xFactor = 1.7f;
float yFactor = 1.5f;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
  xServo.attach(9);
  xServo.write(xServoPos);
  yServo.attach(10);
  yServo.write(yServoPos);
}

void loop() {
  /*if (Serial.available() > 0)
  {
    xServoPos = Serial.readString().toInt();
    if (xServoPos != NULL)
    {
      xServo.write(xServoPos);
    }*/
  if (Serial.available())//  > 0 && xServo.read() == xServoPos
  {
    String incomingData = Serial.readString();
    xEditAmount = (incomingData[2] - '0')*xFactor;
    yEditAmount = (incomingData[3] - '0')*yFactor;
    
    //Serial.println(xEditAmount);
    //Serial.print(incomingData);
    
    if (incomingData[0] == '-' && xServoPos >= 2+xEditAmount)
    {
      xServoPos-=xEditAmount;
    }
    else if (incomingData[0] == '+' && xServoPos <= 180-xEditAmount)
    {
      xServoPos+=xEditAmount;
    }
    
    if (incomingData[1] == '-' && yServoPos >= 45+yEditAmount)
    {
      yServoPos-=yEditAmount;
    }
    else if (incomingData[1] == '+' && yServoPos <= 180-yEditAmount)
    {
      yServoPos+=yEditAmount;
    }
    
    if (xServoPos >= 2 && xServoPos <= 180 && xServoPos != NULL)
    {
      xServo.write(xServoPos);
    }
    
    if (yServoPos >= 45 && yServoPos <= 180 && yServoPos != NULL)
    {
      yServo.write(yServoPos);
    }
  }
  //Serial.println(xServoPos);
}
