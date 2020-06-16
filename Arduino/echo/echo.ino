const int pinLED = 13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pinLED, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    int inByte = Serial.read();
    Serial.println(inByte);
    digitalWrite(pinLED, HIGH);
  }
}
