#include <DigiUSB.h>

void setup()
{
  pinMode(2, INPUT); // P2 = anolog input 1
  pinMode(1, OUTPUT);
  DigiUSB.begin();
}

void loop()
{
  if (!DigiUSB.available()) {
    DigiUSB.delay(10);
    return;
  }

  int lastRead;
  lastRead = DigiUSB.read();
  if (lastRead != '\n') {
    DigiUSB.delay(10);
    return;
  }
  
  digitalWrite(1, HIGH);

  int step;
  float temp;
  step = analogRead(1);
  temp = (float)step*500.0/1024.0-60.0;

  DigiUSB.print("{\"temp\":");
  DigiUSB.print(temp);
  DigiUSB.println("}");
    
  digitalWrite(1, LOW);
  DigiUSB.delay(10);
}

