#define X_STEP_PIN 54
#define X_DIR_PIN 55
#define X_ENABLE_PIN 38
#define X_MIN_PIN 3
#define X_MAX_PIN 2

#define Y_STEP_PIN 60
#define Y_DIR_PIN 61
#define Y_ENABLE_PIN 56
#define Y_MIN_PIN 14
#define Y_MAX_PIN 15

#define Z_STEP_PIN 46
#define Z_DIR_PIN 48
#define Z_ENABLE_PIN 62
#define Z_MIN_PIN 18
#define Z_MAX_PIN 19

#define E_STEP_PIN 26
#define E_DIR_PIN 28
#define E_ENABLE_PIN 24

#define Q_STEP_PIN 36
#define Q_DIR_PIN 34
#define Q_ENABLE_PIN 30

#define DELAY_PASO  40

char vectorChar[3];
void setup() {
  // put your setup code here, to run once:
 pinMode(X_STEP_PIN , OUTPUT);
 pinMode(X_DIR_PIN , OUTPUT);
 pinMode(X_ENABLE_PIN , OUTPUT);
 
 pinMode(Y_STEP_PIN , OUTPUT);
 pinMode(Y_DIR_PIN , OUTPUT);
 pinMode(Y_ENABLE_PIN , OUTPUT);

 pinMode(Z_STEP_PIN , OUTPUT);
 pinMode(Z_DIR_PIN , OUTPUT);
 pinMode(Z_ENABLE_PIN , OUTPUT);
 
digitalWrite(X_ENABLE_PIN , LOW);
digitalWrite(Y_ENABLE_PIN , LOW);
digitalWrite(Z_ENABLE_PIN , LOW);
 
 digitalWrite(13,HIGH);

 digitalWrite(X_DIR_PIN , HIGH);
 digitalWrite(Y_DIR_PIN , HIGH);
 digitalWrite(Z_DIR_PIN , HIGH);

 //

 Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
 String str = Serial.readStringUntil('\n');
String cadena=str.substring(4);
cadena.toCharArray(vectorChar,3);
int n=atoi(vectorChar);
  switch (str[0]) {
    
  case '1':
    //do something when var equals 1
    //Serial.println("Motor 1");
         if(str[2]=='1'){
    digitalWrite(X_DIR_PIN , HIGH);
   }else{
    digitalWrite(X_DIR_PIN , LOW);
   }
    for(int a=0; a<n;a++){
  digitalWrite(X_STEP_PIN , HIGH);
  //Serial.print("va")
  delay(DELAY_PASO);
  digitalWrite(X_STEP_PIN , LOW);
    }
    Serial.println("<OK>");
    break;
    
  case '2':
  Serial.println("Motor 2");
     if(str[2]=='1'){
    digitalWrite(E_DIR_PIN , HIGH);
    digitalWrite(Z_DIR_PIN , HIGH);
   }else{
    digitalWrite(E_DIR_PIN , LOW);
    digitalWrite(Z_DIR_PIN , HIGH);
   }
   for(int a=0; a<n;a++){
  digitalWrite(E_STEP_PIN , HIGH);
  digitalWrite(Z_STEP_PIN , HIGH);
  delay(DELAY_PASO);
  digitalWrite(E_STEP_PIN , LOW);
  digitalWrite(Z_STEP_PIN , LOW);
    }
  Serial.println("<OK>");
    break;

      case '3':
   Serial.println("Motor 3");
   if(str[2]=='1'){
    digitalWrite(Y_DIR_PIN , HIGH);
   }else{
    digitalWrite(Y_DIR_PIN , LOW);
   }
   for(int a=0; a<n;a++){
  digitalWrite(Y_STEP_PIN , HIGH);
  delay(DELAY_PASO);
  digitalWrite(Y_STEP_PIN , LOW);
      }
      Serial.println("<OK>");
    break;
    
  default:
    // if nothing else matches, do the default
    // default is optional
    Serial.println("Error");
    break;
}
  }
}
