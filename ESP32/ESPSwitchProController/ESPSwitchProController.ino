#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
 
#define LED 2
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
 
String receivedData = "";
String lastData = "";
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
 
void setup() {
  Serial.begin(115200); 
  pinMode(LED, OUTPUT);
  while(!Serial){
    delay(100);
  }
  setupDisplay();

  display.clearDisplay();
  display.setCursor(25,30);
  display.println("Waiting");
  display.display(); 
}
 
void loop() {
  if(Serial.available()) { 
    lastData = Serial.readStringUntil('\n');

    display.clearDisplay();
    display.setCursor(25,30);
    display.println(lastData);
    display.display(); 
 
    digitalWrite(LED, HIGH);
  }else{
    digitalWrite(LED, LOW);
  }
 
}
 
void setupDisplay() {
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(INVERSE);
  display.setCursor(25,30);
}