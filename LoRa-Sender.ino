
#include <SPI.h>
#include <LoRa.h>

// LoRa module connections
#define SS_PIN    5
#define RST_PIN   14
#define DIO0_PIN  2

void setup() {
  Serial.begin(115200);

  // Configure the LoRa module and start the radio
  LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);

  while (!LoRa.begin(433E6)) {
    Serial.println("LoRa initialization failed. Retrying...");
    delay(500);
  }

  // Must match the sender's sync word
  LoRa.setSyncWord(0xA5);

  Serial.println("LoRa receiver ready");
  Serial.println("Waiting for incoming data...");
}

void loop() {
  // Check whether a LoRa packet has arrived
  int packetSize = LoRa.parsePacket();

  if (packetSize) {
    String receivedData = "";

    // Read the packet sent by the transmitter
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }

    // Display the received readings on the Serial Monitor
    Serial.print("Received data: ");
    Serial.println(receivedData);

    // Extract voltage and current from the comma-separated data
    int commaIndex = receivedData.indexOf(',');

    if (commaIndex > 0) {
      float voltage = receivedData.substring(0, commaIndex).toFloat();
      float current = receivedData.substring(commaIndex + 1).toFloat();

      Serial.print("Voltage: ");
      Serial.print(voltage, 2);
      Serial.println(" V");

      Serial.print("Current: ");
      Serial.print(current, 2);
      Serial.println(" A");

      // Calculate power from the received readings
      float power = voltage * current;

      Serial.print("Power: ");
      Serial.print(power, 2);
      Serial.println(" W");

      Serial.println("----------------------");
    } else {
      Serial.println("Invalid packet format");
    }

    // Display the received signal strength
    Serial.print("RSSI: ");
    Serial.print(LoRa.packetRssi());
    Serial.println(" dBm");
  }
}

