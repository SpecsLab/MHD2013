#include "eHealth.h"
float ECG = 0;
float GSR = 0;
float AIR = 0;
int ECGfreq = 100;
int GSRAIRfreq = 10;
unsigned long lastsampleECG = 0;
unsigned long lastsampleGSRAIR = 0;
unsigned long time = 0;

// The setup routine runs once when you press reset:
void setup() {
  Serial.begin(115200); 
}

// The loop routine runs over and over again forever:
void loop() {
  
  time = millis();
  
  if (time >= (lastsampleECG + (1000/ECGfreq))){
    
    ECG = eHealth.getECG();
    lastsampleECG = millis();
    
    if (time >= (lastsampleGSRAIR + (1000/GSRAIRfreq))){
      GSR = eHealth.getSkinConductanceVoltage();
      AIR = eHealth.getAirFlow();
      lastsampleGSRAIR = millis();        
    }
 
    Serial.print(ECG);
    Serial.print(";");
    Serial.print(GSR); 
    Serial.print(";");
    Serial.println(AIR);
 
  }
}

