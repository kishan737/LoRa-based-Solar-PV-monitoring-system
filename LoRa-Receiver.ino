
#include <SPI.h>
#include <LoRa.h>

// LoRa module connections
#define SS_PIN    5
#define RST_PIN   14
#define DIO0_PIN  2

void setup() {
  Serial.begin(115200);

  // Set up the LoRa module pins
  LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);

  while (!LoRa.begin(433E6)) {
    // Keep trying until the radio starts
    delay(500);
  }

  // Use the same sync word as the transmitter
  LoRa.setSyncWord(0xA5);
}

void loop() {
  // Check for an incoming packet
  int packetSize = LoRa.parsePacket();

  if (packetSize > 0) {
    String receivedData = "";

    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }

    // Find the comma separating voltage and current
    int commaIndex = receivedData.indexOf(',');

    if (commaIndex > 0) {
      String voltageText = receivedData.substring(0, commaIndex);
      String currentText = receivedData.substring(commaIndex + 1);

      voltageText.trim();
      currentText.trim();

      // Convert both fields to numbers
      char *voltageEnd;
      char *currentEnd;

      float voltage = strtof(voltageText.c_str(), &voltageEnd);
      float current = strtof(currentText.c_str(), &currentEnd);

      // Ignore packets that don't contain two valid numbers
      if (voltageEnd != voltageText.c_str() &&
          *voltageEnd == '\0' &&
          currentEnd != currentText.c_str() &&
          *currentEnd == '\0') {

        // Keep this output format compatible with the Python dashboard
        Serial.print(voltage, 2);
        Serial.print(",");
        Serial.println(current, 2);
      }
    }
  }
}
