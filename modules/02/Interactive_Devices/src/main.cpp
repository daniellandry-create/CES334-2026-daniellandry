#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


// put function declarations here:
//e.g int myFunction(int, int);

const int buttonP = 6;
const int buttonG = 7;
const int swtch_pin = 12;
const int PAC_X = 4, PAC_Y = 5;
//const int GHOST_X = 20, GHOST_Y = 5;

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

uint8_t readDigital(int button_P, int button_G, int switch_pin){
  uint8_t is_pressed = 0;

  if (digitalRead(button_P)){is_pressed |= (1<<0);} // button for pacman
  if (digitalRead(button_G)){is_pressed |= (1<<1);} // button for ghost
  if (digitalRead(switch_pin)){is_pressed |= (1<<2);} // switch for on off?

  return is_pressed;

}

// void sendState(uint16_t state){
//   uint8_t frame[4];
//   frame[0] = 0xAA; //Header byte
//   frame[1] = state & 0xFF; // Low byte
//   frame[2] = (state >> 8) & 0xFF; // High byte
//   frame[3] = frame[0] ^ frame[1] ^ frame[2]; // XOR checksum byte

//   Serial.write(frame, 4);
// }

void sendState(uint16_t state){
  Serial.println(state);
}

void setup() {

  // put your setup code here, to run once:

  Serial.begin(9600);
  pinMode(PAC_X, INPUT);
  pinMode(PAC_Y, INPUT);
  pinMode(buttonP, INPUT_PULLUP);
  pinMode(buttonG, INPUT_PULLUP);
  pinMode(swtch_pin, INPUT_PULLDOWN);

}

void loop() {
  // put your main code here, to run repeatedly:
  // Combine states of joysticks, buttons, and switch into single 16 bit number
  uint16_t state = readJoystick(PAC_X, PAC_Y) /*| (readJoystick(GHOST_X, GHOST_Y) << 4) */ | (readDigital(buttonP, buttonG, swtch_pin) << 8);
  //Serial.printf("JoystickX: %d JoystickY: %d\n",analogRead(PAC_X), analogRead(PAC_Y));
  //Serial.printf("ButtonP: %d ButtonG: %d\n", digitalRead(buttonP), digitalRead(buttonG));
  // Send state to RPi
  sendState(state);
  delay(1000);
}

