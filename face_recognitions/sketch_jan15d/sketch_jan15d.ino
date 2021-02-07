int led_green  = 7;      // for input
int led_blue   = 6;     // for output
int led_yellow = 5;    // for alarm
int led_red    = 4;   // for fake face

int out1       = 8;
int out2       = 9;
int out3       = 10;
int out4       = 11;
int out5       = 12;

char mybyte    = 0; // command byte -128 - 0 -127

void come_in(){
  int on_time = 20;
  digitalWrite(led_green,HIGH);
  delay(on_time);
  digitalWrite(led_green,LOW);
  }
  
void come_out(){
  int on_time = 20;
  digitalWrite(led_blue,HIGH);
  delay(on_time);
  digitalWrite(led_blue,LOW);
  }
  
void warning(){
  int on_time = 20;
  digitalWrite(led_yellow,HIGH);
  delay(on_time);
  digitalWrite(led_yellow,LOW);
  }
  
void alarm(){
  int on_time = 20;
  digitalWrite(led_red,HIGH);
  delay(on_time);
  digitalWrite(led_red,LOW);
  }

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600); // connect to PORT4
pinMode(led_yellow,OUTPUT);
pinMode(led_blue,OUTPUT);
pinMode(led_green,OUTPUT);
pinMode(led_red,OUTPUT);
pinMode(out1,OUTPUT);
pinMode(out2,OUTPUT);
pinMode(out3,OUTPUT);
pinMode(out4,OUTPUT);
pinMode(out5,OUTPUT);

for(int i = 4; i < 8; i ++){
  digitalWrite(i,LOW);
  }
for(int j = 8; j < 13; j ++){
  digitalWrite(j,HIGH);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
    mybyte = Serial.read();

    if(mybyte == 96){
      come_in();
      }
    else if(mybyte == 97){
      come_out();
      }
    else if((mybyte == 98)or (mybyte == 99)){
      warning();
      }
    else if(mybyte == 100){
      alarm();
      }
    }
}
