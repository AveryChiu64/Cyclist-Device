int handle_button = 6;
int led_front = 7;
int led_back = 8;
int buzzer = 9;
int theft_mode_button = 10;
int prevX, currX;

bool toggle_status = false;

void setup() {
  pinMode(led_front, OUTPUT);
  pinMode(handle_button, INPUT);
  pinMode(led_back, OUTPUT); 
  pinMode(buzzer, OUTPUT);
  pinMode(theft_mode_button, INPUT);
}

bool toggle() {
  toggle_status = false;
  if(digitalRead(theft_mode_button) == HIGH) {
    toggle_status = true;
  }
  return toggle_status;
}

bool alarm(int prevX, int currX) {
  if(prevX - currX > 1000) {
    digitalWrite(buzzer, HIGH);
    return true;
   }
  else
  {
    return false;
  }
}

void loop() {
  if(digitalRead(handle_button) == HIGH){
    while(digitalRead(handle_button) == HIGH){
      digitalWrite(led_front, HIGH);
      delay(500);
      digitalWrite(led_front, LOW);
      delay(500);   
    }
   }
   else
   {
      digitalWrite(led_front, LOW);
   }

  if(currX - prevX < -200) {
    digitalWrite(led_back, HIGH);
  }
  else{
    digitalWrite(led_back, LOW);
  }
  
  if(toggle() && alarm(prevX, currX)){
    digitalWrite(buzzer, HIGH);
  }
}
