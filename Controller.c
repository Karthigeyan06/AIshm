#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <HX711.h>


const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";


const char* serverName = "youripwithport";  // replace with your WSL IP

HX711 scale1;
HX711 scale2;

void setup() {
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");

 
  scale1.begin(D5, D6); // DT, SCK for first HX711
  scale2.begin(D7, D8); // DT, SCK for second HX711

  scale1.set_scale();  scale1.tare();
  scale2.set_scale();  scale2.tare();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    http.begin(client, serverName); 
    http.addHeader("Content-Type", "application/json");

    float weight1 = scale1.get_units(5);
    float weight2 = scale2.get_units(5);

    String postData = "{\"sensor1\": " + String(weight1, 2) + ", \"sensor2\": " + String(weight2, 2) + "}";

    int httpResponseCode = http.POST(postData);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    String payload = http.getString();
    Serial.println("Server response: " + payload);

    http.end();
  } else {
    Serial.println("WiFi not connected!");
  }

  delay(5000);
}
