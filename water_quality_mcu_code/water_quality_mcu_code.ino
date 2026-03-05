#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
// Set your WiFi and the machine running Flask (same network)
const char* ssid ="YOUR_WIFI_SSID";
const char* pass ="YOUR_WIFI_PASSWORD";
// Change to your PC IP and port where Flask runs (e.g. python app.py)
const char* server ="http://YOUR_PC_IP:5000/iot/data";


WiFiClient client;
String s ="";

void setup() {
 Serial.begin(9600);
 WiFi.begin(ssid,pass);

 while(WiFi.status() != WL_CONNECTED){
   Serial.print(".");
 }
  Serial.print("connected");

}

void loop() {

 // Read one line from Serial (from Arduino: temperature#TDS#turbidity#pH)
 if(Serial.available()>0){

    while(Serial.available()>0){

      char c = Serial.read();

      s = s+String(c);
      delay(10);
    }
    s.trim();

    Serial.println(s);
 }

   if(WiFi.status()==WL_CONNECTED && s.length()>0){

          HTTPClient http;

          http.begin(client,server);
          http.addHeader("Content-Type", "application/json");
          // POST body: {"data": "28.5#1200#10#7.2"}
           String json_data = "{\"data\":\""+ s +"\"}";

          int httpResponsecode = http.POST(json_data);


          if (httpResponsecode >0){

              String receive = http.getString();
              Serial.println("http response code: " + String(httpResponsecode));


              Serial.println("receive:"+receive);

             }
              else {
                Serial.println("Error in sending post");
              }

           http.end();
   }
   
   s="";
      
   }