//-----------------------------------------------------------------SCROLLING TEXT

/*
-----------------------------------------------------------------------------------------------------------------------------------------
DMD.h - Function and support library for the Freetronics DMD, a 512 LED matrix display panel arranged in a 32 x 16 layout.
Copyright (C) 2011 Marc Alexander (info <at> freetronics <dot> com) http://www.freetronics.com/dmd
-----------------------------------------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------------------------------------
      Installation:
Arduino Uno    P10 Panel
    13 ---------> S / CLK
    11 ---------> R
     9 ---------> nOE / OE
     8 ---------> L / SCLK
     7 ---------> B
     6 ---------> A
   GND ---------> GND


The P10 panel can still turn on without 5V Power Input if it only uses one panel, but to increase brightness it must be added with 5V Power Input. 
5V Power Input must also be used if using more than one P10 Panel.
-----------------------------------------------------------------------------------------------------------------------------------------
*/

#include <SPI.h>       
#include <DMD.h>    
#include <TimerOne.h>  
#include "Arial_black_16.h"
#include "Arial_Black_16_ISO_8859_1.h"
#include "Arial14.h"
#include "SystemFont5x7.h"

#define DISPLAYS_ACROSS 1 //-> Number of P10 panels used, side to side.
#define DISPLAYS_DOWN 1

DMD dmd(DISPLAYS_ACROSS, DISPLAYS_DOWN);

char *Text1 = ""; // text for come in
char *Text2 = ""; // text for come out
char *Text3 = ""; // text for warning
char *Text4 = ""; // text for alarm

int come_in  = 14;
int come_out = 15;
int warning  = 16;
int alarm    = 17;

int state_come_in;
int state_come_out;
int state_warning;
int state_alarm;

//int     interval = 100;    //Speed 100
//long    timer    = start;
//boolean ret      = false;

void ScanDMD() { 
      dmd.scanDisplayBySPI();
    }
    
void setup(void) {
  pinMode(come_in,INPUT);  // loc edit here
  pinMode(come_out,INPUT); // loc edit here
  pinMode(warning,INPUT);  // loc edit here
  pinMode(alarm,INPUT);    // loc edit here
  
  Timer1.initialize(1000);          
  Timer1.attachInterrupt(ScanDMD);   
  dmd.clearScreen(true);   
  Serial.begin(115200);
  }


//loc edit here
void led_come_in(){

  long    start    = millis();
  int     interval = 100;    //Speed 100
  long    timer    = start;
  boolean ret      = false;
    
  Text1 = "WELLCOME";
  dmd.drawMarquee(Text1,strlen(Text1),(32*DISPLAYS_ACROSS)-1,0);

  timer    = start;
  ret      = false;

  while(!ret){
      if ((timer+interval) < millis()) {
        ret   = dmd.stepMarquee(-1,0);
        timer = millis();
        Serial.println(ret);
      }
    }
  }
  

void led_come_out(){

  long    start    = millis();
  int     interval = 100;    //Speed 100
  long    timer    = start;
  boolean ret      = false;
  
  Text2 = "BYE BYE";
  dmd.drawMarquee(Text2,strlen(Text2),(32*DISPLAYS_ACROSS)-1,0);

  timer    = start;
  ret      = false;

  while(!ret){
      if ((timer+interval) < millis()) {
        ret   = dmd.stepMarquee(-1,0);
        timer = millis();
        Serial.println(ret);
      }
    }
  }

void led_warning(){

  long    start    = millis();
  int     interval = 100;    //Speed 100
  long    timer    = start;
  boolean ret      = false;
  
  Text3 = "WARNING";
  dmd.drawMarquee(Text3,strlen(Text3),(32*DISPLAYS_ACROSS)-1,0);

  timer    = start;
  ret      = false;

  while(!ret){
      if ((timer+interval) < millis()) {
        ret   = dmd.stepMarquee(-1,0);
        timer = millis();
        Serial.println(ret);
      }
    }
  }
  
void led_alarm(){

  long    start    = millis();
  int     interval = 100;    //Speed 100
  long    timer    = start;
  boolean ret      = false;
  
  Text4 = "ALARM";
  dmd.drawMarquee(Text4,strlen(Text4),(32*DISPLAYS_ACROSS)-1,0);

  timer    = start;
  ret      = false;

  while(!ret){
      if ((timer+interval) < millis()) {
        ret   = dmd.stepMarquee(-1,0);
        timer = millis();
        Serial.println(ret);
      }
    }
  }

// loc end edit here
  
void loop(void) {
  
  dmd.selectFont(Arial_Black_16_ISO_8859_1);
  //dmd.selectFont(Arial_Black_16);
  //dmd.selectFont(Arial_14);
  //dmd.selectFont(SystemFont5x7);

  //Loc edit here
  state_come_in  = digitalRead(come_in);   //Loc edit here
  state_come_out = digitalRead(come_out);  //Loc edit here
  state_warning  = digitalRead(warning);   //Loc edit here
  state_alarm    = digitalRead(alarm);     //Loc edit here

  if(state_come_in){
    led_come_in();
    }
  else if(state_come_out){
    led_come_out();
    }
  else if(state_warning){
    led_warning();
    }
  else if(state_alarm){
    led_alarm();
    }
}
