#include <WiFi.h>
#include <WiFiUdp.h>
WiFiUDP udp;

// Local network information for ESP32S3
unsigned int localPort = 9999;
// Able to connect to YaleGuest...
// So far unable to connect to yale wireless
const char *ssid = "yale wireless"; // Must have a space!!

// Server connection information
char *serverip = "10.75.70.150";
unsigned int serverport = 8888;

// Buffer for receiving data from server
char packetBuffer[255];

// Photoresistor setup
const int PHOTO_PIN = 18;
const int PHOTO_LOW = 180;
const int PHOTO_HIGH = 4095;
const int PHOTO_SCALE = PHOTO_HIGH - PHOTO_LOW;

void setup() {
  Serial.begin(9600);

  // Set up photo resistor
  pinMode(PHOTO_PIN, INPUT);

  // Connect to yale wireless
  WiFi.disconnect(true); // Erases stored wifi credentials
  WiFi.mode(WIFI_STA); // Accesses wifi as a station
  WiFi.begin(ssid);

  Serial.println("Trying to connect to wifi");

  int max_attempts = 40;
  int attempts = 0;

  while (WiFi.status() != WL_CONNECTED) {
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

  udp.begin(localPort);
  Serial.printf("UPD Client: %s:%i \n", WiFi.localIP().toString().c_str(), localPort);
}

void loop() {
  // Checks for the presence of an incoming UDP packet and reports its size in bytes
  // No packet? -> returns 0

  /*
  int packetSize = udp.parsePacket();
  
  if (packetSize) {
    // Nonzero packet size, so packet has been received
    Serial.print("Received packet from: ");
    // Read the data stored in the packet as a string of chars
    int len = udp.read(packetBuffer, 255);
    Serial.printf("Data: %s\n", packetBuffer);
    Serial.println();
  }
  */

  // Read photoresistor value
  int photo_raw = analogRead(PHOTO_PIN);

  // Clamp the photoresistor value
  int photo_clamped = photo_raw;

  if (photo_raw < PHOTO_LOW) {
    photo_clamped = PHOTO_LOW;
  } else if (photo_raw > PHOTO_HIGH) {
    photo_clamped = PHOTO_HIGH;
  }

  // Scale the photoresistor value
  double photo_scaled = (double) (photo_clamped - PHOTO_LOW) / PHOTO_SCALE;

  // Serial.printf("Photoresistor value: %.5f\n", photo_scaled);

  /*
  Serial.print("[Client Connected] ");
  Serial.println(WiFi.localIP());
  */

  // Start a packet to be sent to the server
  udp.beginPacket(serverip, serverport);
  char buf[30];
  // Write to the buffer
  sprintf(buf, "%.3f", photo_scaled);
  // Add the buffer to the message (needed sprintf to get formatting)
  udp.printf(buf);
  // End the packet, sending it
  udp.endPacket();

}