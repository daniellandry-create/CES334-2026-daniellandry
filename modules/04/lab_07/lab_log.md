# Lab 6 Log - Ryan Fernandes and Daniel Landry

## Action Plan:
 1. Look at stepper motor and servo online documentation
 2. Research example code for program implementation
 3. Write simple test scripts for stepper and servo
 4. Write final program

 ## Execution
 1. Found Arduino libraries for stepper motors and servos
 2. Wrote test script for stepper and servo
 3. Arduino Servo library out of date, decided to focus on stepper first
 4. Stepper motor buzzing as if recieving signal but not moving (not enough power?)
 5. Changed motor, still just buzzing, incorrect esp32->motor driver connections?
 6. Swapped motor driver. Success! The culprit was a faulty motor driver, stepper now rotating properly
 7. Stepper motor speed can't be set to higher than 10 when powered by 5V
 8. Needed to use "ESP32Servo" arduino library, not "Servo"
 9. Servo ground not shared with stepper motor ground, cause eratic behavior in servo
 10. Correction to program regarding servo pattern: "servo_degrees = (servo_degrees + 10) % 190" (instead of "% 180")
 
 ## Video:
 Link: https://youtu.be/LA4RCCqVClI
