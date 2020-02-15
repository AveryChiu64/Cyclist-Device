# makeuoft-hackathon
This repository holds code artifacts for MakeUofT Hackathon 2020

## Arduino Event Publisher
You can create an IOT device using any Arduino compatible prototyping board.  The process is very similar to the steps described in our Raspberry Pi / IOT workshop.  The key is to import and configure an MQTT client library from the Arduino IDE.

The steps for configuring your Arduino IDE environment can be found here:
https://github.com/solacese/car-demo

The above project is related to driving a two-motor remote-control-car using Solace eventing.  The car-kit can be purchased from Amazon.  

You could try to make your own AWS IOT Button hardware using these techniques.  There is a nice Arduino Library named *Ace Button* which implements the de-bounce logic required to detect various button states (clicks, double clicks, button-down, etc). A button in this context is a micro-switch connected to your Arduino board on any of its input pins.  

```
// Example Button Code / Add to your Arduino Project
//
#include <AceButton.h>

const int BUTTON_PIN_1 = D2;

AceButton button1 (BUTTON_PIN_1);

void setup() {
    pinMode(BUTTON_PIN_1, INPUT_PULLUP);
    button1.setEventHandler(handleEvent);
    button1.init(BUTTON_PIN_1, HIGH, 1 /* button id*/);
}

void handleEvent(AceButton* button, uint8_t eventType,
    uint8_t /*buttonState*/) {

  char debugEvent[200];

  // AceButton::kEventPressed
  // AceButton::kEventReleased
  // AceButton::kEventClicked
  // AceButton::kEventDoubleClicked
  // AceButton::kEventLongPressed
  // AceButton::kEventRepeatPressed

  switch (eventType) {
    case AceButton::kEventPressed:      
      Serial.printf("Button %d --- PRESSED !\n", button->getId()); 
      
      if (button->getId() == 1) {
        // Send Event to Solace Event Mesh
        //
        sprintf(debugEvent, "{ 'Button' : %d, 'State' : 'PRESSED' }",  button->getId());
        mqttClient.publish("arduino/button", debugEvent); 
      }
      break;
  }
}
```



