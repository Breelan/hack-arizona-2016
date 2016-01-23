int digiPin = 8;
int joyPin1 = 0;                 // slider variable connecetd to analog pin 0
int joyPin2 = 1;                 // slider variable connecetd to analog pin 1
int value1 = 0;                  // variable to read the value from the analog pin 0
int value2 = 0;                  // variable to read the value from the analog pin 1

void setup() {
  pinMode(digiPin, OUTPUT);              // initializes digital pins 0 to 7 as outputs
  Serial.begin(9600);
}

int treatValue(int data) {
  return (data * 31 / 1024) - 15;
}

 void loop() {
   
  delay(50);
  // reads the value of the variable resistor 
  value1 = analogRead(joyPin1);   
  // this small pause is needed between reading
  // analog pins, otherwise we get the same value twice
  delay(50);             
  // reads the value of the variable resistor 
  value2 = analogRead(joyPin2);   
  
  digitalWrite(digiPin, HIGH); 
  delay(20);  
  digitalWrite(digiPin, LOW);
  delay(20);
  
  int treatVal1 = treatValue(value1);
  int treatVal2 = treatValue(value2);
  
  // Send X,Y,-1 to make formatting easier
  String printVal = String(treatVal1) + ',' + String(treatVal2) + ",-1";
  Serial.println(printVal);
  
 }
