int button_pin = 4;
int switch_pin = 5;
int x_pin = 6;
int y_pin = 7;

void setup() {
  Serial.begin(9600);

  pinMode(button_pin, INPUT_PULLUP);
  pinMode(switch_pin, INPUT_PULLUP);
  pinMode(x_pin, INPUT);
  pinMode(y_pin, INPUT);
}

void loop() {
  int button_val = digitalRead(button_pin);
  int switch_val = digitalRead(switch_pin);
  int x_val = analogRead(x_pin);
  int y_val = analogRead(y_pin);

  Serial.printf("%d,%d,%d,%d\n", button_val, switch_val, x_val, y_val);
  delay(20);
}