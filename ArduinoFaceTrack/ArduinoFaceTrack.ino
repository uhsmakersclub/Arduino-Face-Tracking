#include <Servo.h>

Servo xServo;
Servo yServo;
int xServoPos = 90;
int yServoPos = 90;
int xEditAmount = 0;
int yEditAmount = 0;
int faceSize = 0;
float xFactor = 0.8f;
float yFactor = 0.7f;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  xServo.attach(9);
  xServo.write(xServoPos);
  yServo.attach(10);
  yServo.write(yServoPos);
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available())
  {
    String incomingData = Serial.readString();
    faceSize = (incomingData[4] - '0');
    xEditAmount = ceil((incomingData[2] - '0')*(xFactor+faceSize/6));
    yEditAmount = ceil((incomingData[3] - '0')*(yFactor+faceSize/9));

    if (xEditAmount == 0 && yEditAmount == 0) //laser on
    {
      digitalWrite(13, HIGH);
    }
    else //laser off
    {
      digitalWrite(13, LOW);
    }
    
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
