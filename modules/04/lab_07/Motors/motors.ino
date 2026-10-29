#include <ESP32Servo.h>
#include <Stepper.h>

#define STEPS 2048
Servo myservo;
Stepper mystepper(STEPS, 4, 5, 6, 7);

const int servo_pin = 18;

int servo_degrees = 0;

void setup() {
  Serial.begin(115200);
  myservo.attach(servo_pin);
  mystepper.setSpeed(10);
  myservo.write(servo_degrees);
}

void loop() {
  // Rotate stepper 360 degrees
  mystepper.step(STEPS);

  // Rotate servo 10 degrees
  servo_degrees = (servo_degrees + 10) % 190;
  myservo.write(servo_degrees);
}