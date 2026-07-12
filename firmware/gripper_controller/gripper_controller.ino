#define LED 13
#define RIGHT 12
#define LEFT 11
#define LP 10
#define RP 9

void setup() {
  // put your setup code here, to run once:
  pinMode(LED,OUTPUT);//
  pinMode(RIGHT,OUTPUT);//
  pinMode(LEFT,OUTPUT);//
  pinMode(LP,OUTPUT);//
  pinMode(RP,OUTPUT);//
  digitalWrite(RIGHT,LOW); 
  digitalWrite(LEFT,LOW);
  digitalWrite(LP,LOW);
  digitalWrite(RP,LOW);
  Serial.begin(115200);//连接到串行端口，波特率为9600
  //Serial.setTimeout(1000);
  Serial.println("ready" );
}

void loop() {
  // put your main code here, to run repeatedly:
if(Serial.available())
{
  //delay(1);
  String msg = Serial.readStringUntil('\n');
  //Serial.println(msg);
  // if(msg == "OK")
  // {
  //   digitalWrite(LED,HIGH);
  //   delay(2000);
  //   digitalWrite(LED,LOW);
  // }
  if(msg == "RO")
    digitalWrite(RIGHT,LOW); 
  else if(msg == "RC")
    digitalWrite(RIGHT,HIGH);
  else if(msg == "LO")
    digitalWrite(LEFT,LOW);
  else if(msg == "LC")
    digitalWrite(LEFT,HIGH);
  else if(msg == "AC")
  {
    digitalWrite(RIGHT,HIGH);
    digitalWrite(LEFT,HIGH);
  }
  else if(msg == "AO")
  {
    digitalWrite(RIGHT,LOW);
    digitalWrite(LEFT,LOW);
  }
  else if(msg == "LP")
  {
    digitalWrite(LP,HIGH);
    delay(800);
    digitalWrite(LP,LOW);
  }
  else if(msg == "RP")
  {
    digitalWrite(RP,HIGH);
    delay(800);
    digitalWrite(RP,LOW);
  }
    else if(msg == "AP")
  {
    digitalWrite(LP,HIGH);
    digitalWrite(RP,HIGH);
    delay(800);
    digitalWrite(LP,LOW);
    digitalWrite(RP,LOW);
  }
  else
  {
  }

}

}