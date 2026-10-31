#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


// put function declarations here:
//e.g int myFunction(int, int);

const int button1 = 6;
const int button2 = 7;
const int swtch_pin = 15;
const int PLAYER1_X = 4, PLAYER1_Y = 5;
const int PLAYER2_X = 1, PLAYER2_Y = 2;

const int CENTER = 1800; // Middle of analog read range
const int NEUTRAL_RANGE = 1000; // plus/minus 800 from middle is neutral input

uint8_t readJoystick(int xPin, int yPin){
  int x = analogRead(xPin);
  int y = analogRead(yPin);

  uint8_t bits = 0;

  if (x < CENTER - NEUTRAL_RANGE){ bits |= (1 << 0);}
  if (x > CENTER + NEUTRAL_RANGE){ bits |= (1 << 1);}
  if (y < CENTER - NEUTRAL_RANGE){ bits |= (1 << 2);}
  if (y > CENTER + NEUTRAL_RANGE){ bits |= (1 << 3);}

  return bits;
}

uint8_t readDigital(int button_1, int button_2, int switch_pin){
  uint8_t is_pressed = 0;

  if (digitalRead(button_1) == LOW){is_pressed |= (1<<0);} // button for player 1
  if (digitalRead(button_2) == LOW){is_pressed |= (1<<1);} // button for player 2
  if (digitalRead(switch_pin) == LOW){is_pressed |= (1<<2);} // switch for on off?

  return is_pressed;

}

void sendState(uint16_t state){
  Serial.println(state);
}

void setup() {

  // put your setup code here, to run once:

  Serial.begin(115200);
  pinMode(PLAYER1_X, INPUT);
  pinMode(PLAYER1_Y, INPUT);
  pinMode(PLAYER2_X, INPUT);
  pinMode(PLAYER2_Y, INPUT);
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(swtch_pin, INPUT_PULLUP);

}

void loop() {
  // put your main code here, to run repeatedly:
  // Combine states of joysticks, buttons, and switch into single 16 bit number
  uint16_t state = readJoystick(PLAYER1_X, PLAYER1_Y) | (readJoystick(PLAYER2_X, PLAYER2_Y) << 4) | (readDigital(button1, button2, swtch_pin) << 8);
  sendState(state);
  delay(5);
}

