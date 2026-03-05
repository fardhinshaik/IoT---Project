#define TdsSensorPin A2
#define VREF 5.0      
#define SCOUNT  30    

int analogBuffer[SCOUNT];    
int analogBufferTemp[SCOUNT];
int analogBufferIndex = 0, copyIndex = 0;
float averageVoltage = 0, tdsValue = 0, temperature = 25;


int sensorPin = A0;   
int sensorValue = 0;
float voltage = 0.0;
float turbidity = 0.0;

#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2  

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);


#define PH_PIN A4
float voltage1;
float pH;

void setup() {
  
  Serial.begin(9600);
  pinMode(TdsSensorPin, INPUT);
  sensors.begin();

}

void loop() {

  sensors.requestTemperatures();             
  float tempc = sensors.getTempCByIndex(0);
  float tempf = sensors.toFahrenheit(tempc);

  
  sensorValue = analogRead(sensorPin);

  voltage = sensorValue * (5.0 / 1023.0);

  // turbidity = -1120.4 * voltage * voltage + 5742.3 * voltage - 4352.9;
  turbidity = voltage;


  int raw = analogRead(PH_PIN);
  voltage1 = raw * (5.0 / 1023.0);

 
  pH = 7.0 - (voltage1 - 2.5) * 3.5;

  if (pH < 0) pH = 0;
  if (pH > 14) pH = 14;


  static unsigned long analogSampleTimepoint = millis();
  if (millis() - analogSampleTimepoint > 40U) {  
    analogSampleTimepoint = millis();
    analogBuffer[analogBufferIndex] = analogRead(TdsSensorPin);    
    analogBufferIndex++;
    if (analogBufferIndex == SCOUNT) {
      analogBufferIndex = 0;
    }
  }

  static unsigned long printTimepoint = millis();
  if (millis() - printTimepoint > 800U) {
    printTimepoint = millis();
    for (copyIndex = 0; copyIndex < SCOUNT; copyIndex++) {
      analogBufferTemp[copyIndex] = analogBuffer[copyIndex];
    }
    averageVoltage = getMedianNum(analogBufferTemp, SCOUNT) * (float)VREF / 1024.0; 
    float compensationCoefficient = 1.0 + 0.02 * (tempc - 25.0); 
    float compensationVoltage = averageVoltage / compensationCoefficient; 
    tdsValue = (133.42 * compensationVoltage * compensationVoltage * compensationVoltage - 255.86 * 
                 compensationVoltage * compensationVoltage + 857.39 * compensationVoltage) * 0.5; 
    
  }
  // Backend expects order: temperature#TDS#turbidity#pH (see app.py /iot/data)
  String data = String(tempc)+"#"+String(tdsValue)+"#"+String(turbidity)+"#"+String(pH);

  Serial.println(data);
  delay(1000);
}

int getMedianNum(int bArray[], int iFilterLen) {
  int bTab[iFilterLen];
  for (byte i = 0; i < iFilterLen; i++)
    bTab[i] = bArray[i];
  int i, j, bTemp;
  for (j = 0; j < iFilterLen - 1; j++) {
    for (i = 0; i < iFilterLen - j - 1; i++) {
      if (bTab[i] > bTab[i + 1]) {
        bTemp = bTab[i];
        bTab[i] = bTab[i + 1];
        bTab[i + 1] = bTemp;
      }
    }
  }
  if ((iFilterLen & 1) > 0) {
    bTemp = bTab[(iFilterLen - 1) / 2];
  } else {
    bTemp = (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
  }
  return bTemp;
}