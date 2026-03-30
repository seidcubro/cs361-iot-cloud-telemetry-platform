#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>
#include <DHT.h>

// ---------- SENSOR ----------
#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

// ---------- LED ----------
#define LED_PIN 2  

const char* householdID = "house02";
const char* deviceID = "garage";

// ---------- WIFI ----------
const char* ssid = "INSERT_WIFI_HERE"; 
const char* password = "WIFI_PASSWORD_HERE"; 

// ---------- API ENDPOINT ----------
const char* serverURL = "ENDPOINT_HERE";


// ---------- LED BLINK FUNCTION ----------
void blinkLED(int times, int delayMs) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, LOW);
    delay(delayMs);
    digitalWrite(LED_PIN, HIGH);
    delay(delayMs);
  }
}


// ---------- WIFI ----------
void connectWiFi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    blinkLED(1, 200);  // quick blink while connecting
  }

  Serial.println("WiFi connected");
}


// ---------- FUNCTIONS ----------
float readTemperatureF() {
  for (int i = 0; i < 3; i++) {
    float t = dht.readTemperature(true);
    if (!isnan(t) && t > -40 && t < 185) {
      return t;
    }
    delay(500);
  }
  return NAN;
}

float readHumidity() {
  for (int i = 0; i < 3; i++) {
    float h = dht.readHumidity();
    if (!isnan(h) && h >= 0 && h <= 100) {
      return h;
    }
    delay(500);
  }
  return NAN;
}

void setupTime() {
  configTime(0, 0, "pool.ntp.org");

  while (time(nullptr) < 100000) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nTime synced");
}


// ---------- SETUP ----------
void setup() {

  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  connectWiFi();
  setupTime();

  dht.begin();
}


// ---------- LOOP ----------
void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  float humidity = readHumidity();
  float tempF = readTemperatureF();

  if (isnan(humidity) || isnan(tempF)) {
    Serial.println("Sensor read failed");
    blinkLED(3, 100);  //3 fast blinks = sensor issue
    delay(2000);
    return;
  }

  // ---------- BUILD JSON ----------
  String payload = "{";
  payload += "\"device_id\":\"" + String(deviceID) + "\"";
  payload += ",\"temperature_c\":" + String(tempF);
  payload += ",\"humidity_pct\":" + String(humidity);
  payload += ",\"timestamp\":" + String(time(nullptr));
  payload += "}";

  Serial.println("Payload:");
  Serial.println(payload);

  // ---------- SEND HTTP POST ----------
  HTTPClient http;

  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(payload);

  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);

  String response = http.getString();
  Serial.println(response);

  http.end();

  // ---------- LED STATUS ----------
  if (httpResponseCode >= 200 && httpResponseCode <= 300) {
    blinkLED(1, 500);   //success → slow blink
  } else {
    blinkLED(2, 100);   //error → fast double blink
  }

  delay(60000);
}