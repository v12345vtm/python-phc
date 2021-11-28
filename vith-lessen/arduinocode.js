/*
   This blinks two LEDs independently and not synchronized. Both have other blink frequencies.
   The blink sketches run in two tasks and on two cores.
  https://circuits4you.com/2018/12/31/esp32-devkit-esp32-wroom-gpio-pinout/
  https://randomnerdtutorials.com/esp32-data-logging-temperature-to-microsd-card/


  wifi.txt =  {ssid: "WiFi-2.4-0560", wifipass: "mereldaan", ip: "192.168.1.240" , dns: "192.168.1.1" , gateway: "192.168.1.1" , subnet: "255.2555.255.0"}


   https://i2.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/ESP32-DOIT-DEVKIT-V1-Board-Pinout-36-GPIOs-updated.jpg?quality=100&strip=all&ssl=1


  The time structure is called tm and has teh following values:
  Definition of struct tm:
  Member  Type  Meaning Range
  tm_sec  int seconds after the minute  0-61*
  tm_min  int minutes after the hour  0-59
  tm_hour int hours since midnight  0-23
  tm_mday int day of the month  1-31
  tm_mon  int months since January  0-11
  tm_year int years since 1900
  tm_wday int days since Sunday 0-6
  tm_yday int days since January 1  0-365
  tm_isdst  int Daylight Saving Time flag
  because the values are somhow akwardly defined, I introduce a function makeHumanreadable() where all values are adjusted according normal numbering.
  e.g. January is month 1 and not 0 And Sunday or monday is weekday 1 not 0 (according definition of MONDAYFIRST)

  The functions are inspired by work of G6EJD ( https://www.youtube.com/channel/UCgtlqH_lkMdIa4jZLItcsTg )



  spifsbestanden
  weerurl.txt = http://api.tameteo.nl/index.php?api_lang=nl&localidad=181688&affiliate_id=sy7xtza756tc&v=3.0

  de json decoderen we via  :  https://arduinojson.org/v6/assistant/



  https://www.tameteo.nl/faq.html#vientos

  wifi.txt  = {"ssid": "WiFi-2.4-0560","wifipass": "mereldaan", "ip": "192.168.1.88" , "dns": "192.168.1.1" , "gateway": "192.168.1.1" , "subnet": "255.255.255.0" , "dhcp": "1"  , "websockport": "1337"  , "httpport": "80"}
*/





//////////////class button //eerste echt goede CORE voor peha modules
class Button {
  private:
    byte pin;
    byte flag;
    byte lastflag;
    byte flank; //status : 2= hoog nivo 1=rijzende flank 0=dalende flank
  public:
    Button(byte pin) {
      this->pin = pin;
      lastflag = LOW;
      init();
    }
    void init() {
      pinMode(pin, INPUT); update();
    }
    void update() {
      flag = digitalRead(pin); // read the pushbutton input pin:
      flank = 2 ;
      // compare the SW1flag to its previous state
      if (flag != lastflag) { // if the state has changed, increment the cntr
        if (flag == HIGH) {
          flank = 1;// if the current state is HIGH then the button went from off to on:
        } else {
          flank = 0; // if the current state is LOW then the button went from on to off:
        }
        delay(50); // Delay a little bit to avoid bouncing
      }
      lastflag = flag; // save the current state as the last state, for next time through the loop
    }
    byte getState() {
      update();
      return flag;
    }
    bool isPressed() {
      return (getState() == HIGH);
    }
    bool IsErFlank() {
      update();
      if (flank == 1) //0 is dalende flank en 1 is stijgende flank
      {
        flank = 2 ;//flank is weg zet terug op status2
        return true ;
      }
      else
      {
        return false;
      }
    }
}; // don't forget the semicolon at the end of the class

//PINOUTS used
#define LED1 13
#define LED2 12
#define LED3 14
#define LED4 27
#define LED5 26
#define LED6 25

const int led_pin = 2; //buildinled
//spi
#define SPI_CS 5 //Next, define the microSD card SD pin. In this case, it is set to GPIO 5.
#define SPI_MOSI 23
#define SPI_CLK 18
#define SPI_MISO  19

//i2c rtc
#define I2C_DATA  21
#define I2C_CLK 22
#define DS1307_ADDRESS 0x68
#include "RTClib.h"
RTC_DS1307 rtc;
DateTime nudirect ;
char daysOfTheWeek[7][4] = {"Zo", "Ma", "Di", "Wo", "Do", "Vr", "Za"}; //7 elementen 4char lang
char maandenvhjaar[12][5] = {"Jan", "Feb", "Mrt", "Apr", "Mei", "Jun", "Jul" , "Aug" , "Sep" , "Okt" , "Nov" , "Dec"}; //7 elementen 4char lang
//https://www.tameteo.nl/faq.html#vientos

//i2c lcd
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 20, 4); // set the LCD address to 0x27 for a 16 chars and 2 line display


//#define DEBUG 1
//#define TOONCORE 1
//#define DEBUGTask1 1
//#define DEBUGTask2 1
//#define DEBUGTask3 1
//#define DEBUGTask4 1
//#define DEBUGTask5 1
//#define DEBUGTask6 1
//#define DEBUGSendToRs485 1
//#define DEBUGcrcberekenen 1
//#define  DEBUGonWebSocketEvent  1


TaskHandle_t Task1, Task2 , Task3 , Task4 , Task5  , Task6;



int counter = 3;//hoeveel sec wil je wifi laten proberen te connecteren aan de router
#define tabellengte 17 //hoelang zullen de langste woorden zijn van peha ?
#include <CircularBuffer.h>
CircularBuffer<byte, 120> buffer; //langer woorden van 20bytes zal de peha wss niet uitspreken
//#define testbufferlengte 31
String myArray[tabellengte] ;//tabel die de input opslaat
//byte rs485data[23] = { 0x4A , 0x1 , 0xFF , 0x60 , 0xA5 , 0x4A , 0x1 , 0xFF , 0x60 , 0xA5 , 0x4A , 0x1 , 0xFF , 0x60 , 0xA5 , 0x4A , 0x1 , 0xFF , 0x60 , 0xA5 , 0x4A , 0x1 , 0xFF};
//byte rs485data[testbufferlengte] = { 0xaa , 0xbb , 0x4A , 0x1 , 0xFF , 0x60 , 0xA5 , 0x4A , 0x1 , 0xFF , 0x60 , 0xA5 , 0x4A , 0x1 , 0xFF , 0x60 , 0xA5 , 0x4A , 0x1 , 0xFF , 0x60 , 0xA5 , 0x4A , 0x1 , 0xFF , 0x00 , 0x02 , 0xFF, 0x00, 0xA6, 0xB6};
int elementen = 0;//te waarde hoeveel elementen in ions tabel zitten
int integertabel[tabellengte] ; //ons hex string in decimaal tabel gezet en de crc mee rekent
byte moduleontdekt[255][2];//array met geverifeerde detekties tijdens de broadcast
bool zatEreenBroadcastBij = false;

struct pehaDatapakket {
  String dataZondercrc; // vb "40 01 01"
  String dataMETcrc; // vb "40 01 01 EB C8"
  String crc1; //EB
  String crc2; // C8
  bool verified; //true als de eegegeven parameters voor crc correct waren
};
struct pehaDatapakket PehaDatapakket;

//core (1) interval omdat rts i2c niet werkt op core0task
unsigned long previousMillis = 0;        // will store last time LED was updated
const long interval = 1000;           // interval at which to blink (milliseconds)

//json
#include <ArduinoJson.h>
StaticJsonDocument<30000> doc;
char wifi_json[500]; //hoe lang mag het bestand zij dat ze op de Sd kaart zetten500bytes

//ntp andreas speiss
const char* NTP_SERVER = "be.pool.ntp.org";
const char* TZ_INFO    = "CET-1CEST-2,M3.5.0/02:00:00,M10.5.0/03:00:00";  // enter your brussel time zone (https://remotemonitoringsystems.ca/time-zone-abbreviations.php)
tm timeinfo;
time_t now;
long unsigned lastNTPtime;
unsigned long lastEntryTime;

#include <WiFi.h>
#include <SPIFFS.h>
#include <ESPAsyncWebServer.h>
#include <WebSocketsServer.h>

// Libraries for SD card
#include "FS.h"
#include "SD.h"
#include <SPI.h>

//client voor online zelf REquest te kunnen doen
#include <HTTPClient.h>
String url = "" ; //word overschreven met sd geheugen info weerurl.txt //String url = "http://api.tameteo.nl/index.php?api_lang=nl&localidad=181688&affiliate_id=sy7xtza756tc&v=3.0" ;

// Constants     //char *ssid = "WiFi-2.4-0560";//char *password =  "mereldaan";
String versie = "v38";
int http_port = 80;
int ws_port = 1337;

const char *msg_toggle_led = "toggleLED";
const char *msg_get_led = "getLEDState";


// Globals
AsyncWebServer server(http_port);
WebSocketsServer webSocket = WebSocketsServer(ws_port);
char msg_buf[10];
int led_state = 0;
String Zonopvandaag = "?";
String Zonneervandaag = "?";
String temperatuurvandaag = "?";

//pijltje ophoog voo zonop
#define pijlup 0
byte custompijlomhoogChar[] = {
  B00100,
  B01110,
  B11111,
  B00100,
  B00100,
  B00100,
  B00100,
  B00100
};

#define pijldown 1 //max 7 custom chars
byte custompijlomlaagChar[] = {
  B11011,
  B11011,
  B11011,
  B11011,
  B11011,
  B00000,
  B10001,
  B11011
};

#define kloklogo 2 //max 7 custom chars
byte customkloklogoChar[] = {
  B00100,
  B01110,
  B10101,
  B10101,
  B10111,
  B10001,
  B01110,
  B00100
};

#define weerlogo 3 //max 7 custom chars
byte customweerlogoChar[] = {
  B01000,
  B10100,
  B01000,
  B00000,
  B00000,
  B00000,
  B00000,
  B00000
};

bool error_wifi = false ;
bool error_sd = false ;
bool error_weerurl = false ;
bool error_ntp = false ;
bool error_wifijson = false ;
bool error_i2cRtc = false ;
bool error_spiffs = false ;
bool error_tasks = false ;

byte errorcodeESP = 0; //0 is geen foutcode

/*--------------------------------------------------------*/
/*---------------------- SUBROUTINES ---------------------*/
/*--------------------------------------------------------*/


byte errorcodegenereren()
{
  error_wifi == false ?     bitWrite(errorcodeESP, 0, 0) :  bitWrite(errorcodeESP, 0, 1);
  error_sd == false ?       bitWrite(errorcodeESP, 1, 0) :  bitWrite(errorcodeESP, 1, 1);
  error_weerurl == false ?  bitWrite(errorcodeESP, 2, 0) :  bitWrite(errorcodeESP, 2, 1);
  error_ntp == false ?      bitWrite(errorcodeESP, 3, 0) :  bitWrite(errorcodeESP, 3, 1);
  error_wifijson == false ?  bitWrite(errorcodeESP, 4, 0) :  bitWrite(errorcodeESP, 4, 1);
  error_i2cRtc == false ?    bitWrite(errorcodeESP, 5, 0) :  bitWrite(errorcodeESP, 5, 1);
  error_spiffs == false ?    bitWrite(errorcodeESP, 6, 0) :  bitWrite(errorcodeESP, 6, 1);
  error_tasks == false ?     bitWrite(errorcodeESP, 7, 0) :  bitWrite(errorcodeESP, 7, 1);
  //  relayState ? Relay_ON : Relay_OFF
  //if (relayState) then use Relay_ON otherwise use Relay_OFF
  //  bitWrite(errorcodeESP, 0, 1);  // write 1 to the least significant bit of x
  Serial.print ("errorcodeESP="); // 10000000
  Serial.println(errorcodeESP, BIN); // 10000001
  return errorcodeESP;
}

void updatRTCenWeer()
{
  {
    if ( getNTPtime(1)) {
#ifdef DEBUG // #endif
      Serial.println("NTP naar RTC geupdate");
#endif
      rtc.adjust(DateTime(timeinfo.tm_year + 1900 , timeinfo.tm_mon + 1, timeinfo.tm_mday, timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec));
      Serial.println(" rtc.adjusted");
      webSocket.broadcastTXT("NTp naar RTC geupdate"  );//toon info in webbrower in de console
    } else {
      Serial.println("NTP naar RTC FAILED");
    }
    if ( ! getJSONweerbericht()) {
#ifdef DEBUG // #endif
      Serial.println("upd weerbericht voor vandaag gelukt");
#endif
      webSocket.broadcastTXT("upd weerbericht voor vandaag gelukt"  );//toon info in webbrower in de console
    }
  }
}

void tijdsslotbepalen_LCDvolzetten()
{ //hier zitten we elke sec omwille van de main loop interval
  byte tijdslotmodulo ;//= nudirect.hour() / 3 ; // uuraanduiding modulo 3
  switch (nudirect.hour()) {
    case 23:
    case 0:
    case 22:
      tijdslotmodulo = 7; // vanaf23h
      break;
    case 20:
    case 21:
    case 19:
      tijdslotmodulo = 6;// vanaf20h
      break;
    case 17:
    case 18:
    case 16:
      tijdslotmodulo = 5;// vanaf17h
      break;
    case 14:
    case 15:
    case 13:
      tijdslotmodulo = 4;// vanaf14h
      break;
    case 11:
    case 12:
    case 10:
      tijdslotmodulo = 3;// vanaf11h
      break;
    case 8:
    case 9:
    case 7:
      tijdslotmodulo = 2;// vanaf08h
      break;
    case 5:
    case 6:
    case 4:
      tijdslotmodulo = 1;// vanaf05h
      break;
    case 2:
    case 3:
    case 1:
      tijdslotmodulo = 0;// vanaf02h
      break;
  }

  int actuele_temp =  doc["day"]["1"]["hour"][tijdslotmodulo]["temp"] ;
  String weertext =  doc["day"]["1"]["hour"][tijdslotmodulo]["symbol_description"] ;
  String symbol_description =  doc["day"]["1"]["hour"][tijdslotmodulo]["symbol_description"] ;
  String windspeed =  doc["day"]["1"]["hour"][tijdslotmodulo]["wind"] ["speed"];
  String windrichting =  doc["day"]["1"]["hour"][tijdslotmodulo]["wind"] ["dir"];
  String regen =  doc["day"]["1"]["hour"][tijdslotmodulo]["rain"];
#ifdef DEBUG // #endif
  Serial.print ("windspeed= ");
  Serial.println (windspeed);
  Serial.print ("windrichting= ");
  Serial.println (windrichting);
  Serial.print ("tijdslotmodulo= ");
  Serial.println (tijdslotmodulo);
  Serial.print ("regen= ");
  Serial.println (regen);
#endif
  if ( nudirect.month() < 13) {
    nudirect = rtc.now();//vraag eens aan de rtc hoe laat ist
    lcd.setCursor(0, 2);
    if (nudirect.day() < 10) {
      lcd.print(' ');
    }
    lcd.print(nudirect.day(), DEC);
    lcd.print(' ');
    lcd.print(maandenvhjaar[nudirect.month() - 1 ]);
    lcd.print(' ');
    lcd.setCursor(9, 2);
    if (nudirect.hour() < 10) {
      lcd.print(' ');
    }
    lcd.print(nudirect.hour(), DEC);
    lcd.print(':');
    lcd.print( voorloopnulrtc(nudirect.minute()));
    lcd.print(':');
    lcd.print( voorloopnulrtc(nudirect.second()));
    lcd.print(' ');
    lcd.print(daysOfTheWeek[nudirect.dayOfTheWeek()]);
    lcd.setCursor(15, 1);
    if (actuele_temp > 0) {
      lcd.print(' ');
    }
    lcd.print(actuele_temp);
    lcd.write(weerlogo); // c° logo
     lcd.print(' ');
    lcd.setCursor(0, 1);  //pos , lijn
    lcd.print(WiFi.localIP());
  }
  else {

    if (! rtc.begin()) {
      Serial.println("Couldn't find 2ekeerRTC");
      error_i2cRtc = true ;
    }
    lcd.setCursor(8, 2);
    lcd.print(" ");
    lcd.setCursor(0, 1);  //pos , lijn
    lcd.print(WiFi.localIP());
    // updateDeRTCmetNTP();

    updatRTCenWeer();
    nudirect = rtc.now();//vraag eens aan de rtc hoe laat ist
  }

  lcd.setCursor(0, 3);
  lcd.write(pijlup);
  lcd.print(Zonopvandaag);
  lcd.print(" ");
  lcd.write(pijldown);
  lcd.print(Zonneervandaag);
  lcd.setCursor(0, 0);
  lcd.print("   ");
  lcd.setCursor(0, 0);
  lcd.print(windspeed);
  lcd.setCursor(3, 0);
  lcd.print(windrichting);

  // Serial.println(windrichting);
  // String tst = "tijdslot"  +  String(tijdslotmodulo) ;
  // webSocket.broadcastTXT(tst );//toon info in webbrower in de console
}

///////////////////////////
void updateDeRTCmetNTP() {
  if (WiFi.status() == WL_CONNECTED  && getNTPtime(10) && error_i2cRtc == false)
  {
    error_wifi = false ;
    error_ntp = false ;
    error_i2cRtc = false ;
#ifdef DEBUG // #endif
    Serial.println("NTP naar RTC geupdate");
#endif
    rtc.adjust(DateTime(timeinfo.tm_year + 1900 , timeinfo.tm_mon + 1, timeinfo.tm_mday, timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec));
    lcd.setCursor(0, 1);  //pos , lijn
    lcd.print(WiFi.localIP());
  }
  else {
    Serial.println("error update-DeRTCmetNTP");
  }
}



//getweerbericht in json formaat via url Request op internet
bool getJSONweerbericht()
{
  error_weerurl = false ;
  // String payload = "";
#ifdef DEBUG // #endif
  Serial.print("Request weerbericht");
  Serial.println(url);
#endif
  HTTPClient http;
  http.begin(url); // // http.begin("http://api.tameteo.nl/index.php?api_lang=nl&localidad=181688&affiliate_id=sy7xtza756tc&v=3.0"); //HTTP
  int httpCode = http.GET();  // start connection httpCode will be negative on error
  if (httpCode > 0) {
    // HTTP header has been send and Server response header has been handled.
#ifdef DEBUG // #endif
    Serial.printf("[HTTP] GET... code: %d\n", httpCode);
#endif
    // file found at server
    if (httpCode == HTTP_CODE_OK) {
      //  payload = http.getString();
      //   Serial.println(payload);
      error_weerurl = false ;
      ////////////////////
      File file = SPIFFS.open("/weerbericht.json", FILE_WRITE);
      if (!file) {
        Serial.println("error opening /weerbericht.json");
        error_spiffs = true;
      }
      if (file.print(http.getString())) {
#ifdef DEBUG // #endif
        Serial.println("saved /weerbericht.json");
#endif
      } else {
        Serial.println("writeError /weerbericht.json");
        error_spiffs = true;
      }
      file.close();
      ///////////////////////////////////
    }
  } else {
    Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    error_weerurl = true ;
  }
  http.end();

#ifdef DEBUG // #endif
  Serial.println("closing weerbericht and save to spifs");
#endif

  File gedownloadweerberichtinSpiffs = SPIFFS.open("/weerbericht.json", "r");

  if (!gedownloadweerberichtinSpiffs) {
    Serial.println("Failed to open gedownloadweerberichtinSpiffs");
    //  return;
  }

  Serial.print (gedownloadweerberichtinSpiffs);  Serial.println("*weerbericht _json* parsen");
  // // Deserialize the JSON document naar object doc
  DeserializationError error = deserializeJson(doc, gedownloadweerberichtinSpiffs);
  gedownloadweerberichtinSpiffs.close(); //bestand niet direct meer nodig

  // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    error_weerurl = true ;
  }
  // Fetch values.
  //  String   location = doc["location"];
  //  String   dag1 = doc["day"]["1"]["name"];
  //  String   zon = doc["day"]["1"]["sun"];
  String   zonop =  doc["day"]["1"]["sun"]["in"];
  String   zonneer =  doc["day"]["1"]["sun"]["out"];
  //
  //  String   wind =  doc["day"]["1"]["wind"]["speed"];
  //  String   regen =  doc["day"]["1"]["rain"] ;
  //  String   humidity =  doc["day"]["1"]["humidity"] ;
  //  String   pressure =  doc["day"]["1"]["pressure"] ;
  //-//int actuele_temp =  doc["day"]["1"]["hour"][tijdslotmodulo]["temp"] ; //tijdslotmodulo is de huidig uur gedeeld door 3

  Zonopvandaag =  zonop;
  Zonneervandaag =  zonneer;
  //  temperatuurvandaag = pressure ;
  //
  //
  // Print values.
  //  Serial.println(F("weerbericht op decoded  is="));
  //  Serial.println(location);
  //  Serial.println(dag1);
  //  Serial.println(zon);
  //  Serial.println(zonop);
  //  Serial.println(zonneer); //  //
  //  Serial.println(wind);
  //  Serial.println(regen);
  //  Serial.println(humidity);
  //  Serial.println(pressure);
#ifdef DEBUG // #endif
  Serial.print("weeronline inlezen error_weerurl=");
#endif

  /////////////////arduiojson assistant helper = https://arduinojson.org/v6/assistant/

  JsonObject day = doc["day"];
  /// JsonObject drieuurblok = doc["day"]["hour"];
  //  JsonObject day_1 = day["1"];
  //  const char* day_1_date = day_1["date"]; // "20210304"
  //  const char* day_1_name = day_1["name"]; // "Donderdag"
  //  Serial.println( day_1_name);
  //  String   wind =  doc["day"]["1"]["wind"]["speed"];
  //  String   regen =  doc["day"]["1"]["rain"] ;
  //  String   humidity =  doc["day"]["1"]["humidity"] ;
  //String   tjdslotA =  doc["day"]["1"]["hour"] ;
  //Serial.print ( "tjdslotA");  Serial.println( tjdslotA);

  // String   bb =  doc["day"]["1"]["hour"][1] ;
  // Serial.print ( "bb");  Serial.println( bb); //werkt

  //bb{"interval":"05:00","temp":"3","symbol_value":"3","symbol_description":"Bewolkt","symbol_value2":"3","symbol_description2":"Bewolkt","wind":{"speed":"13","dir":"N","symbol":"9","symbolB":"33","gusts":"23"},"rain":"0","humidity":"78","pressure":"1026","clouds":"56%","snowline":"400","windchill":"0","uv_index":"0"}

  JsonObject elementDAY ;
  JsonObject elementDAY_Tijdslot ;

  for (byte teller = 1 ; teller < 6 ; teller ++)
  {
    elementDAY = day[String(teller)];
    const char* elementDAY_name = elementDAY["name"]; // "Donderdag"
    const char* day_1_tempmin = elementDAY["tempmin"]; // "-1"
    const char* day_1_tempmax = elementDAY["tempmax"]; // "7"
    const char* elementDAY_windspeed = elementDAY["wind"]["speed"]; // 14
    const char* day_1_sun_in = elementDAY["sun"]["in"]; // "07:24"
    const char* day_1_sun_out = elementDAY["sun"]["out"]; // "18:32"
    Serial.print ( "elementDAY_windspeed"); Serial.print ( elementDAY_windspeed);
    Serial.print ( " ");
    Serial.println( elementDAY_name);
    Serial.print ( "  ");
    Serial.print ( "sun_in");  Serial.println( day_1_sun_in);
    Serial.print ( "sun_out");  Serial.println( day_1_sun_out);
    Serial.print ( " tempmin");  Serial.println( day_1_tempmin);
    Serial.print ( " tempmax");  Serial.println( day_1_tempmax);
    //   elementDAY_Tijdslot =  doc["day"]["1"]["hour"][1] ;//werkt
    //    const char* interval = elementDAY_Tijdslot["interval"];
    //    Serial.print ( "interval=");  Serial.println(interval);//
    //    const char* temp = elementDAY_Tijdslot["temp"];
    //    Serial.print ( "temp=");  Serial.println(temp);
    for (byte tellertje = 0 ; tellertje < 8 ; tellertje ++)
    {
      elementDAY_Tijdslot =  doc["day"][String(teller)]["hour"][tellertje] ;
      const char* interval = elementDAY_Tijdslot["interval"];
      const char* temp = elementDAY_Tijdslot["temp"];
      Serial.print ( " interval=");  Serial.print (interval);
      Serial.print ( " temp=");  Serial.print (temp);
      Serial.println();
    }
    // while (1) {}

    //    for (JsonObject elem : elementDAY["hour"].as<JsonArray>())
    //    {
    //      const char* interval = elem["interval"]; // "02:00", "05:00", "08:00",
    //      const char* temp = elem["temp"]; // "4", "4", "
    //      const char* symbol_description = elem["symbol_description"]; // "Bewolkt m
    //      const char* wind_speed =  elem["wind"]["speed"]; // "5", "6", "7", "9", "14", "17", "12", "14"
    //      const char* wind_dir =  elem["wind"]["dir"]; // "NE", "NE", "N
    //      const char* pressure = elem["pressure"]; // "1023", "10
    //      const char* humidity = elem["humidity"]; // "98", "9
    //      const char* rain = elem["rain"]; // "1.1",
    //      Serial.print (interval);
    //      Serial.print (" temp");
    //      Serial.print (temp);
    //      Serial.print (" ");
    //      Serial.print (symbol_description);
    //      Serial.print (" windspeed");
    //      Serial.print (wind_speed);
    //      Serial.print (" winddir");
    //      Serial.print (wind_dir);
    //      Serial.print (" druk");
    //      Serial.print (pressure);
    //      Serial.print (" humidity");
    //      Serial.print (humidity);
    //      Serial.print (" rain");
    //      Serial.print (rain);
    //      Serial.print (" ");
    //      Serial.println();
    //    }
    Serial.print("weeronline inlezen  day-teller"); Serial.println(teller);
  }  /////////einde arduinojson assistanthelper
  return error_weerurl ;
}//end  get-JSONweerbericht


//ntp
bool getNTPtime(int sec) {
  {
    uint32_t start = millis();
    do {
      time(&now);
      localtime_r(&now, &timeinfo);
      Serial.println(".connecting2NTP.");
      delay(10);
    } while (((millis() - start) <= (1000 * sec)) && (timeinfo.tm_year < (2016 - 1900)));
    if (timeinfo.tm_year <= (2016 - 1900)) return false;  // the NTP call was not successful
  }
  return true;
}


void SendToRs485(String inclusiefCRC , bool wisbuffereerst = true )
{
  if (wisbuffereerst == true) {
    buffer.clear();
#ifdef DEBUGSendToRs485 // #endif
    Serial.println("cleared ringbuffer via parameter ");
#endif
  }
  Serial.print("send to peha: ");
  for (int x = 0; x < elementen + 2; x = x + 1) {
    Serial.print (integertabel[x], HEX); //naar rs232 monitor
    Serial.print ("-");
    char karakter = integertabel[x];
    Serial2.print(karakter); //naar rs485 van peha!!
  }
  Serial.println("-");
  vTaskDelay( 5 / portTICK_PERIOD_MS ); // wait for one second zodat peha kan antwoorden voor ons
}///////////////////////////////////////////////////////////////////////////////////////////////////

void naartabel(String data, char separator)
{ //in= string     out = integertabel[x]
  for (int n = 0; n < tabellengte; n++)
  {
    (integertabel[n]) = 0x0c;
    (myArray[n]) = "";
  }
  elementen = 0;
  String myArray2[20];
  int maxIndex = data.length() - 1;
  int strIndex[] = {0, -1};
  for (int i = 0; i <= maxIndex ; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
      // Serial.print(" waarde: ");
      String waarde = data.substring(strIndex[0], strIndex[1]);
      //  Serial.println(waarde); delay(1);
      myArray[elementen] = waarde ;
      elementen++;
    }
  }
  for (int x = 0; x < tabellengte; x = x + 1) {
    char charbuf[4];
    myArray[x].toCharArray(charbuf, 8);
    long int rgb = strtol(charbuf, 0, 16); //=>rgb=255
    integertabel[x] = rgb;
  }
}
///////////////////////////////////////////////////////////////////////


String voorloopnul(byte x)
{ // in:byte 0x0f out : "0F"
  String METvoorloopnul = "";
  METvoorloopnul.reserve(2) ;
  if (x < 0x10) {
    METvoorloopnul = "0" + String(x, HEX) ;
  }
  else
  {
    METvoorloopnul = String(x, HEX) ;
  }
  METvoorloopnul.toUpperCase();
  return METvoorloopnul ;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////

String voorloopnulrtc(byte x)
{
  String METvoorloopnul = "";
  METvoorloopnul.reserve(2) ;
  if (x <  10) {
    METvoorloopnul = "0" + String(x, DEC) ;
  }
  else
  {
    METvoorloopnul = String(x, DEC) ;
  }
  METvoorloopnul.toUpperCase();
  return METvoorloopnul ;
}

////////////////

pehaDatapakket crcberekenen(String hexstring , byte teverifierencrc1 = 0x00 , byte teverifierencrc2 = 0x00 , bool regeldetogglebitautomatisch = false)
{ //in : string "40 01 01"
  //out :alle info inclusief crc zal in een tabel staan : myArray[x]
  if (regeldetogglebitautomatisch == true) {
    byte gewenstetoggleBitvoorDEmodule = moduleontdekt[integertabel[0]][1];
#ifdef DEBUGcrcberekenen //#endif
    Serial.print ("gewenstetoggleBitvoorDEmodule") ; Serial.println(gewenstetoggleBitvoorDEmodule) ;
#endif
    if (gewenstetoggleBitvoorDEmodule == 0 )
    {
#ifdef DEBUGcrcberekenen //#endif
      Serial.println("gewenstetoggleBitvoorDEmodule0 ") ;
      Serial.print("togglebyte ombuigen naar 8x ");
      Serial.print("van"); Serial.println(hexstring);
#endif
      hexstring.setCharAt(3, '8');
#ifdef DEBUGcrcberekenen //#endif
      Serial.print("naar8"); Serial.println(hexstring);
#endif
    }
    else if (gewenstetoggleBitvoorDEmodule >= 1 )
    {
#ifdef DEBUGcrcberekenen //#endif
      Serial.println("gewenstetoggleBitvoorDEmodule 1of3") ;
      Serial.print("togglebyte ombuigen naar 0x ");
      Serial.print("van"); Serial.println(hexstring);
#endif
      hexstring.setCharAt(3, '0');
#ifdef DEBUGcrcberekenen //#endif
      Serial.print("naar0"); Serial.println(hexstring);
#endif
    }
  }
  naartabel(hexstring, ' ' );//een tabel met strings en een tabel met longintegers
  long int tempcrc = 65535 ; //0xFFFF; //'notatie voor 0xFFFF
  for (int i = 0; i < elementen; i = i + 1)
  {
    tempcrc = tempcrc ^ (integertabel[i]); // ^ = xor
    //nu gaan we 8keer schuiven met bytes
    for (int j = 8; j > 0; j = j - 1)
    {
      long int een = 1;
      long int som = tempcrc & een;
      if (som == 0x01) {
        //$temp_crc = ($temp_crc >> 1) ^ 0x8408;
        tempcrc = tempcrc >> 1; // 'bug in vb.net als je deelt door 2 !! niet doen dus beter >>1 bit naar rechts opschuiven
        tempcrc = tempcrc ^ 0x8408;//onze polynoom
      }
      else
      {
        tempcrc = tempcrc / 2;
      }
    }
  }
  tempcrc = tempcrc ^ 65535 ;//0xFFFF 'resultaat is een getal 45053 dec = AFFD hex = crc:>> FD AF
  String sCodeValue = String(tempcrc, HEX);
  // Serial.println (tempcrc , HEX);//crc in decimale weergave
  tempcrc = tempcrc + 65536;// in hex zorgen dat er een voorloopnulis
  // Serial.println (tempcrc , HEX);
  sCodeValue = String(tempcrc, HEX).substring(1, 5); //voorloop1 wegdoen die we hierboven creerden door de +65536 te doen
  // Serial.println (sCodeValue); //nu zien we de crc in hex notatie en met een voorloop "1"
  sCodeValue.toUpperCase() ; //alles in grote letters zetten voor de schoonte
  String crcbyte1 = sCodeValue.substring(2, 4) ;
  String crcbyte2 = sCodeValue.substring(0, 2) ;
  //Serial.print (" crc1= "); Serial.print (crcbyte1); Serial.print (" crc2= "); Serial.println (crcbyte2);
  // Serial.print (" in= "); Serial.println (hexstring); Serial.print (" out= ");
  String crcresultaat = hexstring + " " + crcbyte1 + " " + crcbyte2 ;
  // Serial.println (crcresultaat);
  //tabellen aanlengen met de crc
  myArray[elementen + 0 ] = (crcbyte1);
  myArray[elementen + 1 ] = (crcbyte2);
  //2e keer de tabel maken met de integers
  for (int x = 0; x < tabellengte; x = x + 1) {
    char charbuf[4];
    myArray[x].toCharArray(charbuf, 8);
    long int rgb = strtol(charbuf, 0, 16); //=>rgb=255
    integertabel[x] = rgb;
  }
  //als optie kunnen we ook een crc verifieren die we al kregen van de peha
  PehaDatapakket.dataZondercrc = hexstring ; // vb "40 01 01"
  PehaDatapakket.dataMETcrc = crcresultaat; // vb "40 01 01 EB C8"
  PehaDatapakket.crc1 = crcbyte1;
  PehaDatapakket.crc2 = crcbyte2 ;
  PehaDatapakket.verified = true ;
  if (teverifierencrc1 != teverifierencrc2 )
  { //als het beide 0x00 0x00 was er geen explexiete vraag om te verifieren
    String TC1 = voorloopnul( teverifierencrc1);
    String TC2 = voorloopnul( teverifierencrc2);
    // Serial.print ("berekende crc 's " ); Serial.print (crcbyte1 ); Serial.println (crcbyte2 ); //berekende crc
    // Serial.print ("te controleren ontvangen crc " ); Serial.print (TC1 ); Serial.println (TC2 ); //berekende crc

    if (TC1 == crcbyte1 && TC2 == crcbyte2 )
    {
#ifdef DEBUGcrcberekenen
      Serial.println ("de meegegven crc klopt" );
#endif
      PehaDatapakket.dataZondercrc = hexstring ; // vb "40 01 01"
      PehaDatapakket.dataMETcrc = crcresultaat; // vb "40 01 01 EB C8"
      PehaDatapakket.crc1 = crcbyte1;
      PehaDatapakket.crc2 = crcbyte2 ;
      PehaDatapakket.verified = true ; //berekende crc klopt met de ontvangen crc
    }
    else {
#ifdef DEBUGcrcberekenen
      Serial.println ("de meegegven crc FOUT" );
#endif
      PehaDatapakket.dataZondercrc = hexstring ; // vb "40 01 01"
      PehaDatapakket.dataMETcrc = crcresultaat; // vb "40 01 01 EB C8"
      PehaDatapakket.crc1 = crcbyte1;
      PehaDatapakket.crc2 = crcbyte2 ;
      PehaDatapakket.verified = false ;
    }
  }
  return PehaDatapakket;
}

////////////////////////////

void blink(byte pin, int duration) {
  digitalWrite(pin, HIGH);
  delay(duration);
  digitalWrite(pin, LOW);
  delay(duration);
}

/////////////////////

/***********************************************************
   Functions webserver
*/

// Callback: receiving any WebSocket message
void onWebSocketEvent(uint8_t client_num,
                      WStype_t type,
                      uint8_t * payload,
                      size_t length) {
  // Figure out the type of WebSocket event
  switch (type) {
    // Client has disconnected
    case WStype_DISCONNECTED:
#ifdef DEBUGonWebSocketEvent //#endif
      Serial.printf("[%u] Disconnected!\n", client_num);
#endif
      break;

    // New client has connected
    case WStype_CONNECTED:
      {
        IPAddress ip = webSocket.remoteIP(client_num);
#ifdef DEBUGonWebSocketEvent //#endif
        Serial.printf("[%u] Connection from ", client_num);
        Serial.println(ip.toString());
#endif
      }
      break;

    // Handle text messages from client
    case WStype_TEXT:

      // Print out raw message
#ifdef DEBUGonWebSocketEvent //#endif
      Serial.printf("[%u] Received text: %s\n", client_num, payload);
#endif
      // Toggle LED  we zijn op core1
      if ( strcmp((char *)payload, "toggleLED") == 0 ) {
        led_state = led_state ? 0 : 1;
        Serial.printf("Toggling LED to %u\n", led_state);
        digitalWrite(led_pin, led_state);
        SendToRs485( crcberekenen( "45 01 06" , 0x00 , 0x00 , true ).dataMETcrc); //true wil zeggen pas intructie aan ifv togglebit voor die module
        //tijdrtcvragen();//werkt ook niet juist
        // Serial.print  ("core=" );
        // Serial.println ( xPortGetCoreID());

        // Report the state of the LED
      } else if ( strcmp((char *)payload, "getLEDState") == 0 ) {
        sprintf(msg_buf, "%d", led_state);
        Serial.printf("Sending to [%u]: %s\n", client_num, msg_buf);
        webSocket.sendTXT(client_num, msg_buf);

        // send data to all connected clients
        webSocket.broadcastTXT(msg_buf  );


        // Message not recognized
      } else {
        Serial.println("[%u] Message not recognized");
      }
      break;

    // For everything else: do nothing
    case WStype_BIN:
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
    default:
      break;
  }
}

// Callback: send homepage
//void onIndexRequest(AsyncWebServerRequest *request) {
//  IPAddress remote_ip = request->client()->remoteIP();
//  Serial.println("[" + remote_ip.toString() +   "] HTTP GET request of " + request->url());
//  request->send(SPIFFS, "/index.html", "text/html");
//}

// Callback: send style sheet
//void onCSSRequest(AsyncWebServerRequest *request) {
//  IPAddress remote_ip = request->client()->remoteIP();
//  Serial.println("[" + remote_ip.toString() +
//                 "] HTTP GET request of " + request->url());
//  request->send(SPIFFS, "/style.css", "text/css");
//}

String getContentType(String filename) { // convert the file extension to the MIME type
  if (filename.endsWith(".html")) return "text/html";
  else if (filename.endsWith(".css")) return "text/css";
  else if (filename.endsWith(".js")) return "application/javascript";
  else if (filename.endsWith(".ico")) return "image/x-icon";
  else if (filename.endsWith(".json")) return "application/json";
  return "text/plain";
}

////v12345vtm gewoon weegave van spiffs statische paginas
//bool debugonPageNotFound(AsyncWebServerRequest *request) { // send the right file to the client (if it exists)
//  String path  = request->url();
//  Serial.println("handleFileRead: " + path);
//  if (path.endsWith("/")) path += "index.html";         // If a folder is requested, send the index file
//  String contentType = getContentType(path);            // Get the MIME type
//  if (SPIFFS.exists(path)) {                            // If the file exists
//    File file = SPIFFS.open(path, "r");                 // Open it
//
//    ////SPIFFS, "/style.css", "text/css"  200, contentType, file
//    request->send(SPIFFS, path, contentType); // And send it to the client
//    file.close();                                       // Then close the file again
//    return true;
//  }
//  Serial.println("\tFile Not Found");
//  request->send(404, "text/plain", "Not found in spiffs");
//  return false;                                         // If the file doesn't exist, return false
//}

//v12345vtm gewoon weegave args




bool onPageNotFound(AsyncWebServerRequest *request) { // send the right file to the client (if it exists) first check it on spiffs , then on sd card
  String path  = request->url();
  Serial.println("handleFileRead: " + path);
  int paramsNr = request->params(); //zijn er via formulier of actieve url , parameters meegeven in de url vd browser ? vb : http://192.168.1.88/?action=input&STM=0&MOD=3&CHA=5&EVT=4
  Serial.println(paramsNr);
  if (paramsNr  > 1) {
    for (int i = 0; i < paramsNr; i++) {
      AsyncWebParameter* p = request->getParam(i);
      Serial.print("Param name: ");
      Serial.println(p->name()); //http://192.168.1.88/?action=input&STM=0&MOD=3&CHA=5&EVT=4
      Serial.print("Param value: ");
      Serial.println(p->value()); // http://192.168.1.88/?user=tt&device=vv
      Serial.println("------");
    }
    request->send(200, "text/plain", "message received from" + path );
  }
  else
  {
    if (path.endsWith("/")) path += "index.html";         // If a folder is requested, send the index file
    String contentType = getContentType(path);            // Get the MIME type

    if (SPIFFS.exists(path))
    { // If the file exists on spiffs
      File file = SPIFFS.open(path, "r");                 // Open it
      //SPIFFS, "/style.css", "text/css"  200, contentType, file
      request->send(SPIFFS, path, contentType); // And send it to the client
      file.close();    // Then close the file again
      Serial.println("spifss read: " + path);
      return true;
    }

    if (SD.exists(path))
    { // 2e poging If the file exists on sd
      File file = SD.open(path, "r");                 // Open it
      request->send(SD, path, contentType); // And send it to the client
      file.close();                                       // Then close the file again
      Serial.println("sdcard read: " + path);
      return true;
    }


    Serial.println("\tFile Not Found");
    request->send(404, "text/plain", "Not found in spiffs or sd");
    return false;  // If the file doesn't exist (no spiffs , no SDcard, return false
  }
}

/*--------------------------------------------------*/
/*---------------------- Tasks ---------------------*/
/*--------------------------------------------------*/
void codeForTask1( void * parameter )
{
  for (;;) {
    blink(LED1, 600);
    delay(500);//de esp32 vertaald het naar vtaskdelay  // vTaskDelay(800);
    error_tasks = false;
#ifdef TOONCORE // #endif
    Serial.print("Task 1:   running on core");
    Serial.println (xPortGetCoreID());
#endif
    if (WiFi.status() != 3) {
      //   Serial.print ("wifi:nok ");
      error_wifi = true ;
    }
    if (SD.begin(SPI_CS) != 1 ) {
      //   Serial.print ("sd:nok ");
      error_sd = true ;
    }
    if (nudirect.month() > 12 ) {
      //   Serial.print ("rtc=tilt");
      error_i2cRtc = true ;
    }
    //    if (SD.begin(SPI_CS) == 1 ) {
    //      Serial.print ("  ");
    //    }
    //    if (SD.begin(SPI_CS) == 1 ) {
    //      Serial.print ("  ");
    //    }
    //    if (SD.begin(SPI_CS) == 1 ) {
    //      Serial.print ("  ");
    //    }
    //    if (SD.begin(SPI_CS) == 1 ) {
    //      Serial.print ("  ");
    //    }
    //    if (SD.begin(SPI_CS) == 1 ) {
    //      Serial.print ("  ");
    //    }
    Serial.println ();
  }
}

/////

void codeForTask2( void * parameter )
{
  for (;;) {
    blink(LED2, 500);
    error_tasks = false;
    vTaskDelay(50);
#ifdef TOONCORE // #endif
    Serial.print("Task 2: running on core");
    Serial.println (xPortGetCoreID());
#endif

    String modulegezien;
    for (byte i = 0; i < 255 ; i++) {
      if ( moduleontdekt[i][0] == 1 )
      {
        modulegezien = modulegezien + "(" + String(i , HEX ) + "toggle:" + String( moduleontdekt[i][1] ) + ") " ;
      }
    }
    if (zatEreenBroadcastBij == true) {
      Serial.println("");
      Serial.print ("(module/togglebit)"); Serial.println (modulegezien);
    }
    else {
      Serial.println("");
      Serial.print (" moduleontdekt[i]=\t"); Serial.println (modulegezien);
    }
  }
}

/////////////////////////////////////////

void codeForTask3( void * parameter )
{
  for (;;) {
    error_tasks = false;
    blink(LED3, 50);
    vTaskDelay(50);
#ifdef DEBUGTask3 // #endif
    //  Serial.print("\t\t\tTask 3: running on core");
    //  Serial.println (xPortGetCoreID());
#endif
    /////////////////////////////////////////////
    String modnr ;


    if (buffer.size() > 5 ) {
      /////////buffer shiften indien we de eerste bytes net binnen kregen of kwijt raakten
#ifdef DEBUGTask3 // #endif
      Serial.print ( "\n buffer.size= "); Serial.println( buffer.size());
#endif
      bool zitframegoed = false;
      String gezienpakketmetcrc = "";// voorloopnul( buffer[ n ]) + " ";
      String gezienpakketZONDERcrc = "";
      do {
        for (byte n = 0; n <= buffer.size()   ; n++)
        {
#ifdef DEBUGTask3 // #endif
          Serial.print("decodeerbuffer n="); Serial.print (n); Serial.print("=data= ");// Serial.print ( buffer[ n] , HEX);
          Serial.print ( buffer[ n] , HEX);
          Serial.print(" : ");
#endif
          byte   togglebitnibble   = buffer[ n ] >> 4;
          byte   aantaldatabytesdievolgentnibble   = buffer[ n ] << 4; //wis de higher nibble
          aantaldatabytesdievolgentnibble   = aantaldatabytesdievolgentnibble >> 4;
          //  Serial.print(" togglebitnibble "); Serial.print  ( togglebitnibble , HEX);
          if ((togglebitnibble == 0x00   ||  togglebitnibble == 0x08) &&  buffer[ n ] > 0 )
          {
#ifdef DEBUGTask3 // #endif
            Serial.print(" mogelijks togglebyte= "); Serial.print (togglebitnibble , HEX);
            Serial.print("  ; bytes dievolgen= "); Serial.println( aantaldatabytesdievolgentnibble , HEX);
            //als we een togglebyte zien op moet dit minimum op de 2e element zijn .
            //als we het op de 1e element al zien , wil het zeggen dat we een adresbyte kwijt zijn
#endif


            if (n != 1) {
              Serial.print(" togglebyte zit nog niet op 2e element in ringbuffer\n\n\n ");
              for (byte el = 2; el <= n   ; el++)
              {
#ifdef DEBUGTask3 // #endif
                Serial.println("shift ");
#endif
                buffer.shift(); //potentiele togglebyte opschuiven tot hij de 2e element is in de ringbuffer
              }
#ifdef DEBUGTask3 // #endif
              Serial.print (" *0e element is  nu*"); Serial.println( buffer[ 0 ] , HEX);
              // n=0; //herbeginnen

              for (byte nn = 0; nn <= buffer.size()   ; nn++)
              {
                Serial.print ( buffer[ nn] , HEX);
                Serial.print("-");
              }
#endif
              zitframegoed = true ; // tis verschoven tot het goed komt
              break;
            }


            if (n == 1)
            {
#ifdef DEBUGTask3 // #endif
              Serial.print("sjance we zitten frame goed en moeten niet shiften ");
#endif
              zitframegoed = true ;
              break;
            }
          }
          else {
#ifdef DEBUGTask3 // #endif
            Serial.print(" data  "); Serial.println( buffer[n] , HEX);
#endif
          }
        }
      } while (!zitframegoed );
      //1e packet uitfilteren/////////////////////////////

      byte pakketlengtemetcrc =  buffer[ 1 ] << 4 ;
      pakketlengtemetcrc = pakketlengtemetcrc >> 4 ; //hoger nibble wegschuiven en terug
      pakketlengtemetcrc = pakketlengtemetcrc + 4 ;
#ifdef DEBUGTask3 // #endif
      Serial.print("\n  byte met lengteaanduiding  "); Serial.println( buffer[ 1 ] );
      Serial.print("\n  berekende pakketlengtemetcrc+4=  "); Serial.println(pakketlengtemetcrc);
#endif
      for   (byte aa = 0; aa <= pakketlengtemetcrc - 1  ; aa++)
      { //als de togglebyte er is ,testen we eens hoelang het pakket is en of het een geldige crc heeft
        gezienpakketmetcrc = gezienpakketmetcrc +  voorloopnul( buffer[ aa]) + " ";
        //   Serial.print(" generereer pakket  "); Serial.println( buffer[aa] , HEX);
      }

      for   (byte aa = 0; aa <= pakketlengtemetcrc - 3  ; aa++)
      {
        //als de togglebyte er is ,testen we eens hoelang het pakket is en of het een geldige crc heeft
        gezienpakketZONDERcrc = gezienpakketZONDERcrc +  voorloopnul( buffer[ aa]) + " ";
        //   Serial.print(" generereer pakket  "); Serial.println( buffer[aa] , HEX);

      }
#ifdef DEBUGTask3 // #endif
      Serial.print(" 1e pakket    met crc  = "); Serial.println( gezienpakketmetcrc);
      Serial.print(" 1e pakket zonder crc  = "); Serial.println( gezienpakketZONDERcrc);
#endif
      //doe een crc verifcatie van de 1e bytes die je kan herkennen

      if (crcberekenen(gezienpakketZONDERcrc ,  buffer[ pakketlengtemetcrc - 2 ]  , buffer[pakketlengtemetcrc - 1 ] , false).verified)
      {
        Serial.println(" juistecrc  = ");
        Serial.println(buffer[ pakketlengtemetcrc - 2 ] ,  HEX);
        Serial.println(buffer[ pakketlengtemetcrc - 1 ] , HEX);
      }
      else
      {
        Serial.println(" foute crc  = ");
        Serial.println(buffer[ pakketlengtemetcrc - 2 ] ,  HEX);
        Serial.println(buffer[ pakketlengtemetcrc - 1 ] , HEX);
        Serial.println("break weg !! loop forever to debug");
      }


#ifdef DEBUGTask3 // #endif
      /////duplicates uitzoeken////////////////////////////
      Serial.println("\n\n find duplicate crc's :");
      for (byte n = 0; n <= buffer.size()   ; n++)
      {
        byte offset = n + pakketlengtemetcrc;
        if (buffer[ offset + 0 ] == buffer[ pakketlengtemetcrc - 2  ] && buffer[offset + 1] == buffer[pakketlengtemetcrc - 1 ]  )
        {
          Serial.print("0e crc blok=");
          Serial.print(buffer[  pakketlengtemetcrc - 2 ] , HEX);  Serial.print("_");
          Serial.print(buffer[   pakketlengtemetcrc - 1] , HEX);

          Serial.print(" blockscan=");
          Serial.print(buffer[  offset - 3 ] , HEX); Serial.print("_");
          Serial.print(buffer[  offset - 2 ] , HEX); Serial.print("_");
          Serial.print(buffer[  offset - 1] , HEX);  Serial.print("_");
          Serial.print(buffer[  offset + 0 ] , HEX); Serial.print("_");
          Serial.print(buffer[  offset + 1 ] , HEX); // Serial.print("_");

          Serial.print (" we vonden een gelijke paketten die starten op pos=" );
          byte startvaneenduplikaatpakket = n + pakketlengtemetcrc - 2 ;
          Serial.println (startvaneenduplikaatpakket);
          for (byte k = startvaneenduplikaatpakket - 1; k <= startvaneenduplikaatpakket +   pakketlengtemetcrc - 2 ; k++)
          {
            //   Serial.print(" wissen als je 't  kan=");   Serial.print (k); Serial.print(" - ");   Serial.println(buffer[ k] , HEX);
          }

        }
      }
      ////////////////////////////////////
#endif

      Serial.println ( "\n pakket ontleden op broadcast , buffersize="); Serial.println( buffer.size());
      //        if (buffer[ n + 1 ] == 0x01 && buffer[ n + 2] == 0xff ) =                             Serial.print("broadcastpatroon outg mod start op"); Serial.println(n);
      //        if (buffer[ n + 1 ] == 0x02 && buffer[ n + 2] == 0xff && buffer[ n + 3] == 0x00 ) =   Serial.print("INPUTbroadcastpatroon start op");
      //        if (buffer[ n + 1 ] == 0x02 && buffer[ n + 2] == 0xff && buffer[ n + 3] == 0xfc ) =   Serial.print("mmc/busschak broadcastpatroon start op"); Serial.println(n);

      Serial.print(" 1e pakket zonder crc  = "); Serial.println( gezienpakketZONDERcrc);
      //hier chrasht het soms

      for (byte k = 0; k <=   pakketlengtemetcrc - 2 ; k++)
      {
        Serial.print("zoek of t ene soort broadcast is");   Serial.print (k); Serial.print(" - ");   Serial.println(buffer[ k] , HEX);

        if (buffer[ k + 1 ] == 0x01 && buffer[ k + 2] == 0xff )
        {
          Serial.println ( "\n outp broadcast ");
          moduleontdekt[buffer[ k ]][0] = 1 ; // aanvinken dat we echt die module gezien hebben
          modnr = voorloopnul(buffer[ k ]);
          SendToRs485( crcberekenen(modnr + " 03 FE 00 FF" , 0x00 , 0x00 , false ) .dataMETcrc); //buffer niet preventief wissen eer je data zend want strax zenden we nog een ack
          break;
        }


        if (buffer[ k + 1 ] == 0x02 && buffer[ k + 2] == 0xff && buffer[ k + 3] == 0x00 )
        {
          Serial.println ( "\n inp broadcast ");

          moduleontdekt[buffer[ k ]][0] = 1 ; // aanvinken dat we echt die module gezien hebben
          modnr = voorloopnul(buffer[ k ]);
          SendToRs485( crcberekenen(modnr + " 03 FE 00 FF" , 0x00 , 0x00 , false ) .dataMETcrc); //buffer niet preventief wissen eer je data zend want strax zenden we nog een ack
          break;

        }

        if (buffer[ k + 1 ] == 0x02 && buffer[ k + 2] == 0xff && buffer[ k + 3] == 0xfc )
        {
          Serial.println ( "\n busschak en mmc broadcast ");
          moduleontdekt[buffer[ k ]][0] = 1 ; // aanvinken dat we echt die module gezien hebben
          modnr = voorloopnul(buffer[ k ]);
          SendToRs485( crcberekenen(modnr + " 0D FC 00 1F 00 00 02 12 22 32 42 52 62 72" , 0x00 , 0x00 , false ) .dataMETcrc); // incl all inputs enablenen
          break;

        }


        else {
          Serial.println ( "\n TIS EEN STATUS OF ACTIE , maar zeker gene brodcast , dus we moeten ontleden ");
          break;
        }


      }


      Serial.print("bepaald  1e pakket zonder crc  = "); Serial.println( gezienpakketZONDERcrc);
      ///////////////////////onleden status
      if (true)
      {
        Serial.println ( "geldige crc gezien in de module feedback (geen broadcast) : ") ;
        byte modulenummer = buffer[0] ;// == de module die iets te zeggen had
        byte modulekategorie = 0xFF ; //kip tegen de muur
        byte hoeveelbytesVolgenEr;

        if ((buffer[1] >> 4) == 0 or (buffer[1] >> 4) == 8)
        { //inputcontrole of het een geldige byte is die we controleren
          moduleontdekt[buffer[0]][1] = bitRead(buffer[1], 7) ; //toggle bit opslaan in de tabel op lokatie van de mod adres
          //   Serial.print("geldige togglebit gezien"); Serial.println(tog);
          hoeveelbytesVolgenEr = buffer[1] ; //tussen 1 en 15
          bitClear(hoeveelbytesVolgenEr, 7) ;//togglebit wegdoen
        }

        if (modulenummer >= 0 && modulenummer <= 0 + 31 ) {
          modulekategorie = 0x00;
        }
        if (modulenummer >= 32 && modulenummer <= 32 + 31 ) {
          modulekategorie = 0x20;
        }
        if (modulenummer >= 64 && modulenummer <= 64 + 31 ) {
          modulekategorie = 0x40;
        }
        if (modulenummer >= 96 && modulenummer <= 96 + 31 ) {
          modulekategorie = 0x60;
        }
        if (modulenummer >= 128 && modulenummer <= 128 + 31 ) {
          modulekategorie = 0x80;
        }
        if (modulenummer >= 160 && modulenummer <= 160 + 31 ) {
          modulekategorie = 0xa0;
        }
        if (modulenummer >= 192 && modulenummer <= 192 + 31 ) {
          modulekategorie = 0xc0;
        }
        if (modulenummer >= 224 && modulenummer <= 224 + 31 ) {
          modulekategorie = 0xe0;
        }

        //   feedback op statusaanvragen doen
        switch (modulekategorie) {
          case 0x00:
            //   statements 02 04 01 FF 00 00 81 08
            Serial.println("\t\t\tingangmod");
            Serial.println("\t\t\tbytesVolgenEr:" + ( hoeveelbytesVolgenEr , DEC));
            Serial.println("\t\t\ttogglebit:" + moduleontdekt[buffer[0]][1]);
            if (hoeveelbytesVolgenEr == 1) {
              Serial.println("\t\t\tiemand drukt op knop in muur");
              Serial.println("\t\t\twelkeknop werd gedrukt="); Serial.print( buffer[2] , HEX);// 62 is knop6 functie2
              SendToRs485( crcberekenen( voorloopnul(modulenummer) + " 01 00" , 0x00 , 0x00 , false ).dataMETcrc); //true wil zeggen pas intructie aan ifv togglebit voor die module
            }
            if (hoeveelbytesVolgenEr == 4) {
#ifdef DEBUGTask3 // #endif
              Serial.println("\t\t\tmod st.");
              Serial.println("\t\t\tleduitg0-7="); Serial.print( buffer[2] , HEX);
              Serial.println("\t\t\tleduitg8-15="); Serial.print( buffer[3] , HEX);
              Serial.println("\t\t\tknop0-7="); Serial.print( buffer[4] , HEX);
              Serial.println("\t\t\tknop8-15="); Serial.print( buffer[5] , HEX);
#endif
            }
            break;

          case 0x20:
            //   statements
            Serial.println("\t\t\tmmc/ir/busschak mod"); Serial.print("bytesVolgenEr:" ); Serial.println(hoeveelbytesVolgenEr , DEC );
            Serial.print("\t\t\ttogglebit:"); Serial.println( moduleontdekt[buffer[0]][1]);

            if (hoeveelbytesVolgenEr == 1) {
              Serial.println("\t\t\tiemand drukt op knop buschak in muur");
              Serial.print("\twelkeknop werd gedrukt="); Serial.println( buffer[2] , HEX);// 62 is knop6 functie2
              byte knop = (buffer[2] >> 4); // vb 6
              byte functie = (buffer[2] << 4);  //vb 2 is aan>1sec
              functie = (functie >> 4);  //vb 2 is aan>1sec
#ifdef DEBUGTask3 // #endif
              Serial.print ("\t\t\tmodule");
              Serial.println (modulenummer, HEX);
              Serial.print ("\t\t\tknop");
              Serial.println (knop);
              Serial.print ("\t\t\tfunction");
              Serial.println (functie);
#endif
              //   SendToRs485( crcberekenen( voorloopnul(modulenummer) + " 01 00" , 0x00 , 0x00 , true ).dataMETcrc); //true wil zeggen pas intructie aan ifv togglebit voor die module
              // SendToRs485( crcberekenen( voorloopnul(modulenummer) + " 01 00" , 0x00 , 0x00 , false ).dataMETcrc); //true wil zeggen pas intructie aan ifv togglebit voor die module
              SendToRs485( crcberekenen( voorloopnul(modulenummer) + " 01 00" , 0x00 , 0x00 , false ).dataMETcrc); //true wil zeggen pas intructie aan ifv togglebit voor die module
            //  Serial.print ( "\t\t\tpreclear ringbuffersize= "); Serial.println (buffer.size());
              buffer.clear();    Serial.print ( "clear ringbuffer size= "); Serial.println (buffer.size());
            }

            // 22_82_42_52_EE_F7 busschak kan ook 2bytes sturen
            if (hoeveelbytesVolgenEr == 2) {
              Serial.println("\t\t\tte testen busschak2byteskan meer functies dan gewonen ingangod  : vb UIT2 >sec u > 01 ");
              Serial.print ("\t\t\tleduitg0-7="); Serial.println( buffer[2] , HEX);
              Serial.print ("\t\t\tleduitg8-15="); Serial.println( buffer[3] , HEX);
            }


            if (hoeveelbytesVolgenEr == 8) {
#ifdef DEBUGTask3 // #endif
              Serial.println("\t\t\tte testen buscchak8bytes");
              Serial.print ("\t\t\tleduitg0-7="); Serial.println( buffer[2] , HEX);
              Serial.print ("\t\t\tleduitg8-15="); Serial.println( buffer[3] , HEX);
              Serial.print ("\t\t\tleduitg16-23="); Serial.println( buffer[5] , HEX);
              Serial.print ("\t\t\tleduitg24-31="); Serial.println( buffer[5] , HEX);
              Serial.print ("\t\t\tknop0-7="); Serial.println( buffer[4] , HEX);
              Serial.print ("\t\t\tknop8-15="); Serial.println( buffer[5] , HEX);
              Serial.print ("\t\t\tknop16-23="); Serial.println( buffer[5] , HEX);
              Serial.print ("\t\t\tknop24-31="); Serial.println( buffer[5] , HEX);
#endif
            }


            SendToRs485( crcberekenen( voorloopnul(modulenummer) + " 01 00" , 0x00 , 0x00 , true ).dataMETcrc); //true wil zeggen pas intructie aan ifv togglebit voor die module
            break;

          case 0x40:
            //  42 02 01 04 5B 39 oudrelais
            //   44 88 01 00 81 00 00 01 01 20 B2 DB nieuwrelais
            //    4A 03 01 00 15 C0 7A jrm
            Serial.print("uitg mod"); Serial.print("bytesVolgenEr:" ); Serial.print(hoeveelbytesVolgenEr , DEC ); Serial.print("togglebit:"); Serial.print( moduleontdekt[buffer[0]][1]);
            if (hoeveelbytesVolgenEr == 2) {
              Serial.println("oude firmware in uitgmod");
              Serial.print ("relaisstand="); Serial.println( buffer[3] , HEX);
            }
            if (hoeveelbytesVolgenEr == 8) {
#ifdef DEBUGTask3 // #endif
              Serial.print("\t\t\trecente firmware in uitgmod");
              Serial.print("\t\t\trelaisstand="); Serial.println( buffer[4] , HEX);
              Serial.print("\t\t\tterugmeldingenstand="); Serial.println( "?");
              Serial.print("\t\t\tbedrijfsuren="); Serial.println( "?");
#endif
            }
            if (hoeveelbytesVolgenEr == 3) {
#ifdef DEBUGTask3 // #endif
              Serial.print("\t\t\trolluik uitgmod");
              Serial.print("\t\t\trelaisstand="); Serial.println( buffer[4] , HEX);
              Serial.print("\t\t\tterugmeldingenstand="); Serial.println( "?");
#endif
            }
            if (hoeveelbytesVolgenEr == 1) {
#ifdef DEBUGTask3 // #endif
              Serial.print(F("\t\t\tverkeerdelijk hebben we een opdracht aanzien als feedback uitgmod"));
#endif
            }
            break;

          case 0x60:
            //      statements
            Serial.print("\t\t\tanal mod"); Serial.print("bytesVolgenEr:" ); Serial.print(hoeveelbytesVolgenEr , DEC ); Serial.print("togglebit:"); Serial.println( moduleontdekt[buffer[0]][1]);
            break;

          case 0x80:
            //   statements
            Serial.print("\t\t\tmultimod"); Serial.print("bytesVolgenEr:" ); Serial.print(hoeveelbytesVolgenEr , DEC ); Serial.print("togglebit:"); Serial.println( moduleontdekt[buffer[0]][1]);
            break;

          case 0x0a:
            //   A0 05 01 FF FF 03 00 64 5F
#ifdef DEBUGTask3 // #endif
            Serial.print("\t\t\tdimmermod"); Serial.print("bytesVolgenEr:" ); Serial.print(hoeveelbytesVolgenEr , DEC ); Serial.print("togglebit:"); Serial.println( moduleontdekt[buffer[0]][1]);
            Serial.print("\t\t\tdim0stand="); Serial.println( buffer[3] , HEX);
            Serial.print("\t\t\tdim1stand="); Serial.println( buffer[4] , HEX);
            Serial.print("\t\t\tdim0terugmeld="); Serial.println( buffer[5] , HEX);
            Serial.print("\t\t\tdim1terugmeld="); Serial.println( buffer[6] , HEX);
#endif
            break;

          case 0xE0:
            //   statements
            Serial.print("\t\t\tdcf77 mod"); Serial.print("hoeveelbytesVolgenEr:" + ( hoeveelbytesVolgenEr , DEC)); Serial.print("togglebit:"); Serial.println( moduleontdekt[buffer[0]][1]);
            break;

          case 0xC0:
            //   statements
            Serial.println("ongekend");//maar we misbruiken deze range door onze buffer naar hier te resseten na anayyse
            break;

          default:
            //    statements
            // clearRS485ontvangst();
            break;
        }
                buffer.clear();    Serial.print ( "clear ringbuffer size= "); Serial.println (buffer.size());

      }
      // } // end if



      ///////////////////stop ontleden status

    }


  }
}

/////////////////////////////

void codeForTask4( void * parameter )
{
  for (;;) {
    blink(LED4, 50);
    error_tasks = false;
    vTaskDelay(50);
#ifdef TOONCORE // #endif
    Serial.print("\t\t\t\tTask 4: running on core");
    Serial.println (xPortGetCoreID());
#endif
    String inData = "";//recieve rs232 instructie van raspi of gebruiker zoals 40 01 01<lf>
    while (Serial.available() > 0)
    {
      char recieved = Serial.read(); // Process message when new line character is recieved
      if (recieved == '\n')
      {
        String temp = (crcberekenen(inData , 0x00 , 0x00 , true ).dataMETcrc); //pehaDatapakket crcberekenen(String hexstring , byte teverifierencrc1 = 0x00 , byte teverifierencrc2 = 0x00)
#ifdef DEBUG
        Serial.println("\t\t\t\tReceived instructie: "); //
        Serial.print("\t\t\t\tString InData :\t");
        Serial.println(inData);
        Serial.print("\t\t\t\tString InData met crc :\t");
        Serial.println(temp);
#endif
        // webSocket.broadcastTXT("Received rs232instructie:" );//toon info in webbrower in de console
        // webSocket.broadcastTXT(inData );//toon info in webbrower in de console
        SendToRs485(temp , true); //true wil zeggen , dat de ringbuffer leeg mag gedaan worden net voor hij rs485 zend nr de modules
      }
      else
      {
        inData += recieved;
#ifdef DEBUG // #endif
        Serial.println ("\t\t\t\t\n");//clear rs232 monitor :)
#endif
      }
    }
  }
}

//////////////////////////////

void codeForTask5( void * parameter )
{
  for (;;) {
    error_tasks = false;
    blink(LED5, 55);
    vTaskDelay(50);
#ifdef TOONCORE // #endif
    Serial.print(F("\t\t\t\t\tTask 5: running on core"));
    Serial.println (xPortGetCoreID());
#endif
    // als er rs485 data is zet het erbij in de buffer
    if (Serial2.available() > 0 ) {
      delay(3); //we mogen niet te rap data verwerken die binnekomt
      while (Serial2.available() > 0)
      {
#ifdef DEBUG // #endif
        Serial.print ( ">"); // soms komt er ne byte trager binnen dan een andere
#endif
        buffer.push(Serial2.read());
      }
#ifdef DEBUG // #endif
      Serial.print ( "\t\t\t\t\treadRS485-buffersize= "); Serial.println (Serial2.available());
      Serial.print ( "\t\t\t\t\tringbuffersize= "); Serial.println (buffer.size());
#endif
      Serial.print(millis());  Serial.println("\t\t\t\t\t<timestamp:");
      Serial.print ( "\t\t\t\t\tringbuffersize= "); Serial.println (buffer.size());
      for (byte i = 0; i < buffer.size() ; i++) {
        Serial.print(buffer[i], HEX); Serial.print("_");
      }
      Serial.println("_");
    }
  }
}

void codeForTask6( void * parameter )
{
  for (;;) {
    error_tasks = false;
    Button button1(36);
    Button button2(36);
    Button button3(36);
    blink(LED6, 60);
    vTaskDelay(50);
#ifdef TOONCORE // #endif
    Serial.print("\t\t\t\t\t\tTask 6: running on core");
    Serial.println (xPortGetCoreID());
#endif
    if ( button1.IsErFlank())
    {
      Serial.print ("\t\t\t\t\t\tbut1 mod46 0.6 omsch");
      if (true ) {
        SendToRs485( crcberekenen( "45 01 06" , 0x00 , 0x00 , true ).dataMETcrc); //true wil zeggen pas intructie aan ifv togglebit voor die module
      }
      else {
        SendToRs485( crcberekenen( "46 81 66" , 0x00 , 0x00 , true).dataMETcrc);
      }
    }
    if ( button2.IsErFlank())
    {
      Serial.print ("\t\t\t\t\t\tbut2 mod45 omsch relais0 45.00");
      if (true ) {
        SendToRs485( crcberekenen( "45 81 06" , 0x00 , 0x00 , true ).dataMETcrc);
      }
      else {
        SendToRs485( crcberekenen( "45 81 06" , 0x00 , 0x00 , true ).dataMETcrc);
      }
    }
    if ( button3.IsErFlank())
    {
      Serial.print ("\t\t\t\t\t\tbut3 mod45 getfb");
      if (true ) {
        SendToRs485( crcberekenen( "45 01 01" , 0x00 , 0x00 , true ).dataMETcrc);
      }
      else {
        SendToRs485( crcberekenen( "45 01 01" , 0x00 , 0x00 , true ).dataMETcrc);
      }
    }
  }
}


void printDirectory(File dir, int numTabs) {
  while (true) {
    File entry =  dir.openNextFile();
    if (! entry) {      // no more files
      break;
    }
    for (uint8_t i = 0; i < numTabs; i++) {
      Serial.print('\t');
    }
    Serial.print(entry.name());
    if (entry.isDirectory()) {
      Serial.println("/");
      printDirectory(entry, numTabs + 1);
    } else {      // files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
    }
    entry.close();
  }
}

/*--------------------------------------------------*/
/*---------------------- init ---------------------*/
/*--------------------------------------------------*/
void setup() {

  // Init LED and turn off
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, LOW);

  Serial.begin(115200);
  Serial2.begin(19200, SERIAL_8N2);//rs485 peha bus A en B

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
  pinMode(LED6, OUTPUT);
  // Init LED and turn off
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, LOW);

  for (byte i = 0; i < 255; i++) {
    moduleontdekt[i][0] = 0x02; //2insteken omdat we dan zeker iets hebben die niet is aangeraakt geweest in het proces
    moduleontdekt[i][1] = 0x03; // moduletogglebitstand 3insteken omdat we dan zeker iets hebben die niet is aangeraakt geweest in het proces
  }

  lcd.init();    // initialize the lcd
  lcd.clear();
  lcd.backlight();
  lcd.setCursor(0, 0);  //pos , lijn
  lcd.print("start..");
  lcd.print(versie);
  //create lib met custom lcd chars
  lcd.createChar(0, custompijlomhoogChar);
  lcd.createChar(1, custompijlomlaagChar);
  lcd.createChar(2, customkloklogoChar);
  lcd.createChar(3, customweerlogoChar);

  // lcd.home();

  lcd.setCursor(0, 1);
  lcd.write(pijlup);  //  lcd.write(byte(0)); //werkt ooj voor custom  lcdchar
  lcd.write(pijldown);
  lcd.write(kloklogo);
  lcd.write(weerlogo);

  delay(1500);
  lcd.clear();

  ///sd card via spi
  SD.begin(SPI_CS);
  if (!SD.begin(SPI_CS)) {
    Serial.println("Card Mount Failed");
    error_sd = true ;
  }

  uint8_t cardType = SD.cardType();
  if (cardType == CARD_NONE) {
    Serial.println("No SD card attached");
    error_sd = true ;
  }

  File root = SD.open("/");
  printDirectory(root, 0);
  root.close();
  Serial.println("checks for sd card inhoud done");

  // Check to see if the file exists: to get wifi ssid / pasword from user
  if (SD.exists("/wifi.txt")) {
#ifdef DEBUG // #endif
    Serial.println("/wifi.txt json exists.");
#endif
  } else {
#ifdef DEBUG // #endif
    Serial.println("/wifi.txt  json doesn't exist.");
#endif
    error_wifijson = true ;

  }

  if (SD.exists("/weerurl.txt")) {
#ifdef DEBUG // #endif
    Serial.println("/weerurl.txt  string exists.");
#endif
  } else {
#ifdef DEBUG // #endif
    Serial.println("/weerurl.txt  string doesn't exist.");
#endif
    error_weerurl ==  true;
  }

  // re-open the file for reading:
  File myFile = SD.open("/wifi.txt");
  if (myFile) {
    Serial.println("/wifi.txt: inhoud=");
    byte index = 0;
    Serial.print ("filesize: ");
    Serial.println(myFile.size());
    while (myFile.available()) {
      char c = myFile.read();
      wifi_json[index++] = c;
    }
    myFile.close();
  }
  else
  { // if the file didn't open, print an error:
#ifdef DEBUG // #endif
    Serial.println("error opening /wifi.txt vul je sd kaart in of mss langer dan 500bytes?");
#endif
    error_wifijson = true ;
  }

  // open the file for reading:
  File urlfile = SD.open("/weerurl.txt");
  if (urlfile) {
    url = urlfile.readStringUntil('\r'); // cr lf url= http://api.tameteo.nl/index.php?api_lang=nl&localidad=181688&affiliate_id=sy7xtza756tc&v=3.0
#ifdef DEBUG // #endif
    Serial.print("filesize: ");
    Serial.println(urlfile.size());
    Serial.println("/weerurl.txt: inhoud=" );
    Serial.println(url );
#endif
    urlfile.close();
  }
  else
  {
#ifdef DEBUG // #endif
    Serial.println("error opening /weerurl.txt vul je sd kaart in of mss langer dan 500bytes?");
#endif
    error_weerurl = true ;
  }
#ifdef DEBUG // #endif
  Serial.print (wifi_json);  Serial.println("*wifi_json*");
#endif
  // // Deserialize the JSON document naar object doc
  DeserializationError error = deserializeJson(doc, wifi_json);
  // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    error_wifijson = true ;
  }
  // Fetch values.
  String   ss = doc["ssid"];
  String   wifipasstt = doc["wifipass"];
  String   fixedipadres = doc["ip"];
  String   klantdns = doc["dns"];
  String   klantgateway = doc["gateway"];
  String   klantsubnet = doc["subnet"];
  String   websockport = doc["websockport"];
  String   httpport = doc["httpport"];

#ifdef DEBUG // #endif
  Serial.print(F("json op sdkaart is=\n"));
  Serial.println(ss);
  Serial.println(wifipasstt);
  Serial.println(fixedipadres);
  Serial.println(klantdns);
  Serial.println(klantgateway);
  Serial.println(klantsubnet);
  Serial.println(websockport);
  Serial.println(httpport);
  Serial.print(F("json ontleed"));
#endif

  http_port = httpport.toInt(); //80; via json op sd kaart
  ws_port = websockport.toInt(); //1337;

  naartabel(fixedipadres, '.') ; // vb 192.168.1.240 via json op sd kaart //Serial.println(F("converted ip to int"));//  Serial.println(myArray[0]);  Serial.println(myArray[1]);  Serial.println(myArray[2]);  Serial.println(myArray[3]);
  //IPAddress ip(192, 168, 1, 88);
  IPAddress ip(myArray[0].toInt(), myArray[1].toInt(), myArray[2].toInt(), myArray[3].toInt());

  naartabel(klantdns, '.') ; // vb 192.168.1.240 via json op sd kaart //Serial.println(F("converted ip to int"));//  Serial.println(myArray[0]);  Serial.println(myArray[1]);  Serial.println(myArray[2]);  Serial.println(myArray[3]);
  //IPAddress dns(192, 168, 1, 1);
  IPAddress dns(myArray[0].toInt(), myArray[1].toInt(), myArray[2].toInt(), myArray[3].toInt());

  naartabel(klantgateway, '.') ; // vb 192.168.1.240 via json op sd kaart //Serial.println(F("converted ip to int"));//  Serial.println(myArray[0]);  Serial.println(myArray[1]);  Serial.println(myArray[2]);  Serial.println(myArray[3]);
  //IPAddress dns(192, 168, 1, 1);
  IPAddress gateway(myArray[0].toInt(), myArray[1].toInt(), myArray[2].toInt(), myArray[3].toInt());


  naartabel(klantsubnet, '.') ; // vb 192.168.1.240 via json op sd kaart //Serial.println(F("converted ip to int"));//  Serial.println(myArray[0]);  Serial.println(myArray[1]);  Serial.println(myArray[2]);  Serial.println(myArray[3]);
  //IPAddress dns(192, 168, 1, 1);
  IPAddress  subnet(myArray[0].toInt(), myArray[1].toInt(), myArray[2].toInt(), myArray[3].toInt());


  char char_arrayss[ss.length() + 1]; //char_arraypw bestemming en readline is een bronstring
  ss.toCharArray(char_arrayss, ss.length() + 1);
  char char_arraypw[wifipasstt.length() + 1]; //char_arraypw bestemming en readline is een bronstring
  wifipasstt.toCharArray(char_arraypw, wifipasstt.length() + 1);

#ifdef DEBUG // #endif
  Serial.print (char_arrayss);  Serial.println("*via sd ssid*");
  Serial.print (char_arraypw);  Serial.println("*via sd password*");
#endif


  // Connect to Wi-Fi hardcoded
  //IPAddress ip(192, 168, 1, 88);
  //IPAddress dns(192, 168, 1, 1);//dns1 en dns2
  //IPAddress gateway(192, 168, 1, 1);
  //IPAddress subnet(255, 255, 255, 0);
  WiFi.config(ip, gateway, subnet, dns , dns ); //This is important for ntp! Include dns1 and dns2 when configuring!
  WiFi.begin(char_arrayss, char_arraypw);//via sd kaart

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Connecting to WiFi..");
    Serial.println(counter);
    counter--;
    if (counter == 0 )
    {
      Serial.print("geen wifi of geen code");
      error_wifi = true ;
      break;
    }
  }

  // Make sure we can read the SPIFFS file system
  if ( !SPIFFS.begin()) {
#ifdef DEBUG // #endif
    Serial.println("Error mounting SPIFFS");
#endif
    error_spiffs = true ;
  }

#ifdef DEBUG // #endif
  File file = SPIFFS.open("/test.txt", FILE_WRITE);
  if (!file) {
    Serial.println("There was an error opening the file for writing");
  }
  if (file.print("TEST")) {
    Serial.println("spiffs File was written");
  } else {
    Serial.println("spiffs File write failed");
  }
  file.close();
#endif

  //ntp configureren internet time
  configTime(0, 0, NTP_SERVER);
  setenv("TZ", TZ_INFO, 1);

  Serial.println(versie);
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    error_i2cRtc = true ;
  }

  if ( !rtc.isrunning()) {
    Serial.println("RTC is NOT running, let's set the time!");
    //// following line sets the RTC to the date & time this sketch was compiled
    error_i2cRtc = false ;
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // // This line sets the RTC with an explicit date & time, for example to set
    // // January 21, 2014 at 3am you would call:
    //  // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  } else
  {
    Serial.println("RTC is okay running ");
  }

  if (WiFi.status() == WL_CONNECTED   )
  {
    updatRTCenWeer();
    //  getJSONweerbericht(); //get weerberichtvoorspellng  en zet het op sdkaart

    // als default behandelen we  requests for pages that we do not  know if it exists
    server.onNotFound(onPageNotFound);
    // Start web server met cors disabled ,You just have to add this just before your server.begin() !!
    DefaultHeaders::Instance().addHeader("Access-Control-Allow-Origin", "*");
    server.begin();    // Start WebSocket server and assign callback

    webSocket.begin();
    webSocket.onEvent(onWebSocketEvent);
    error_wifi = false ;
  }







#ifdef DEBUG
  Serial.println( "");
  Serial.println( crcberekenen("40 01 01" , 0xeb , 0xc8 , false).dataMETcrc);
  Serial.println( "");
  Serial.println( crcberekenen("40 01 01" , 0xec , 0xc8 , false).verified);
  Serial.println( "");
  Serial.println( crcberekenen("40 01 01" , 0x00 , 0x00 , false ).dataMETcrc);
  Serial.println( "");
  Serial.println( crcberekenen("22 0D FC 00 1F 00 00 02 12 22 32 42 52 62 72" , 0x00 , 0x00 , false ).dataMETcrc);
  Serial.println( "");
  Serial.println(PehaDatapakket.dataZondercrc);
  Serial.println(PehaDatapakket.dataMETcrc);
  Serial.println(PehaDatapakket.crc1);
  Serial.println(PehaDatapakket.crc2);
  Serial.println(PehaDatapakket.verified);
  Serial.print ("setup running on core");
  Serial.println (xPortGetCoreID());
#endif

  xTaskCreatePinnedToCore(
    codeForTask1,
    "led1Task",
    3000,
    NULL,
    0, //prior 0is low 3ishigh
    &Task1,
    0);//core0
  delay(500);  // needed to start-up task1

  xTaskCreatePinnedToCore(
    codeForTask2,
    "led2Task",
    1000,
    NULL,
    1,
    &Task2,
    0);
  delay(500);  // needed to start-up task1

  xTaskCreatePinnedToCore(
    codeForTask3,
    "led3Task",
    7000,
    NULL,
    1,
    &Task3,
    0);
  delay(500);  // needed to start-up task1

  xTaskCreatePinnedToCore(
    codeForTask4,
    "led4Task",
    1000,
    NULL,
    1,
    &Task4,
    0);
  delay(500);  // needed to start-up task1

  xTaskCreatePinnedToCore(
    codeForTask5,
    "led5Task",
    1000,
    NULL,
    1,
    &Task5,
    0);
  delay(500);  // needed to start-up task1

  xTaskCreatePinnedToCore(
    codeForTask6,
    "led6Task",
    1000,
    NULL,
    1,
    &Task6,
    0);


  //check welke modules er al zouden aan liggen
  for (byte i = 65; i < 80 ; i++) {
    //        if ( moduleontdekt[i][0] == 1 )
    //        {
    //          modulegezien = modulegezien + "(" + String(i , HEX ) + "toggle:" + String( moduleontdekt[i][1] ) + ") " ;
    //        }
    SendToRs485( crcberekenen( voorloopnul(i) + " 01 01" , 0x00 , 0x00 , false ).dataMETcrc ,   true );
    delay(500);

  }


}

/*--------------------------------------------------*/
/*---------------------- LOOP DE NIKS DOET core 1 ---------------------*/
/*--------------------------------------------------*/

void loop() {
  webSocket.loop();

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    // interval hier staan we elke seconde in core1
    //hou het hier kort omdat de webserver ale prior moet hebben
    //maar i2c moet hier omdat we in core0 niet lukken

    tijdsslotbepalen_LCDvolzetten(); //tijd  komt van interne realtimeklok

    if (nudirect.hour()  == 6 && nudirect.minute() == 45  && ( nudirect.second() == 35  ||  nudirect.second() == 36  )     )
    {
      updatRTCenWeer();
      lcd.setCursor(18, 3);  //8e kar lijn 3
      lcd.print("#");
    }

    // String x = String(millis() / 1000);
    //  String x = String(errorcodegenereren(), HEX);
    //  webSocket.broadcastTXT( x );//toon info in webbrower in de console
  } //einde interval 1sec

}//end loop