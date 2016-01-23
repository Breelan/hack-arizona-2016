
// Example by Tom Igoe

import processing.serial.*;

Serial myPort;
String inCoord = "";
int[] coordXY;

void setup() {
  size(400, 400);
  // List all the available serial ports
  printArray(Serial.list());

  myPort = new Serial(this, Serial.list()[3], 9600);
  myPort.bufferUntil('\n');
  background(50);
}

void draw() {
  if (myPort.available() > 0) {
    inCoord = myPort.readStringUntil('\n');
    
    // The following if-statement ensures the
    // data will be in proper format for parsing.
    if (inCoord != null) {
      
      print(inCoord);
      
      // Parse the Serial.read
      coordXY = int(split(inCoord, ','));
      
      // The following if-statement ensures
      // the data is parsed properly!
      if (coordXY.length >=2) {
        
        fill(random(0, 255), random(0, 255), random(0, 255));
        ellipse(width/2 + ((coordXY[0])*10), height/2 + ((coordXY[1])*10), 20, 20);
      }
    }
  }
}