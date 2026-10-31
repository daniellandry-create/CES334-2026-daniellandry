#include <WiFi.h>
#include <WiFiUdp.h>
#include <ESPmDNS.h>
#include <map>
#include <cstdint>
WiFiUDP udp;

const int PHOTO_PIN = 16;
const int DIV_PIN = 15;

// Local network information on ESP32S3
unsigned int localPort = 9999;

//std::map<resistances, branches>

// RPi IP address
IPAddress piIP(10, 67, 75, 220);

// Must have a space!!
const char *ssid = "yale wireless"; 

const int32_t BIRD_ID = 1;

// Struct to keep track of a bird's state
struct BirdState {
  int id;
  int branch;
  double volume;
};

//BirdState birds[5];          // index 0 to 4 holds bird IDs 1 to 5
// Create bird for this esp
BirdState bird = {BIRD_ID, -1, 0.0f};
// Server Connection information
unsigned int serverPort = 8888;

// Photoresistor constants
const int PHOTO_LOW = 180;
const int PHOTO_HIGH = 4095;
const int PHOTO_SCALE = PHOTO_HIGH - PHOTO_LOW;

// Voltage divider constants
const int NUM_BRANCHES = 12;
const double DIV_THRESHOLDS[12] = {0.31, 0.44, 0.61, 0.81, 1.10, 1.38, 1.66, 1.98, 2.25, 2.50, 2.72, 3.0};

// Branch 0 is 330 ohm, branch id's increase with resistance value

//buffer for recieving data from server
char packetBuffer[255];

// Function for adding bird to map
// void addBird(int32_t id, int32_t branch, float volume) {
//   birds[id] = {id, branch, volume};   // 0 = not heard yet
// }

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  WiFi.disconnect(true); // Erases stored wifi credentials
  WiFi.mode(WIFI_STA); // Accesses wifi as a station
  WiFi.begin(ssid);

  Serial.println("Trying to connect to WiFi");

  int max_attempts = 40;
  int attempts = 0;

  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");

    attempts += 1;

    if (attempts > max_attempts) {
      Serial.println("\nReached max attempts. Trying again...");
      WiFi.disconnect(true);
      WiFi.begin(ssid);

      attempts = 0;
    }
  }
    // Add bird to mapping
    // addBird(0, 3, 5.0f);
    // addBird(1, 7, 10.0f);
    // addBird(2, 11, 15.0f);
    // addBird(3, 13, 20.0f);
    // addBird(4, 17, 25.0f);
    
    udp.begin(localPort);
    Serial.printf("UDP Client: %s:%i \n", WiFi.localIP().toString().c_str(), localPort);

    // Serial.println("Finding pi's IP");
    // // Find pi's IP address
    // while (piIP == IPAddress()) {        // 0.0.0.0 means not found
    //   piIP = MDNS.queryHost("melody-pi");
    //   if (piIP == IPAddress()) {
    //     Serial.print(".");
    //     delay(1000);  // wait, then try again
    //   }
  Serial.print(bird.id);
  Serial.println("");
  Serial.println("RPi IP: ");
  Serial.println(piIP);

  pinMode(PHOTO_PIN, INPUT);
  pinMode(DIV_PIN, INPUT);
}

void loop() {
  // Photo resistor reading
  int photo_raw = analogRead(PHOTO_PIN);
  int photo_clamped = photo_raw;

  if (photo_raw < PHOTO_LOW) {
    photo_clamped = PHOTO_LOW;
  } else if (photo_raw > PHOTO_HIGH) {
    photo_clamped = PHOTO_HIGH;
  }

  double volume = (double) (photo_clamped - PHOTO_LOW) / PHOTO_SCALE;

  // Voltage divider reading
  int div_raw = analogRead(DIV_PIN);
  double div_voltage = (div_raw / 4096.0) * 3.3;

  int branch_id = -1;

  for (int i = 0; i < NUM_BRANCHES; i++) {
    if (div_voltage < DIV_THRESHOLDS[i]) {
      branch_id = i;
      break;
    }
  }

  // Update state of bird
  updateBirdState(branch_id, volume);

  Serial.printf("Volume: %lf, Branch Id: %d, Photo Raw: %d, Div Volts: %lf\n", volume, branch_id, photo_raw, div_voltage);

  sendBird();
  delay(500);
}

// Send state of one bird as 12 unsigned 8-bit integers
void sendBird() {
  udp.beginPacket(piIP, serverPort);
  udp.write((const uint8_t*)&bird, sizeof(BirdState));
  udp.endPacket();
}

void updateBirdState(int branch, double volume){
  bird.branch = branch;
  bird.volume = volume;
}
