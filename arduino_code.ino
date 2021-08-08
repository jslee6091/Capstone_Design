// 도어락 모터와 연결된 핀
int green = 8;
int red = 9;

// piezo buzzer 핀
int piz = 4;
// switch 핀
int swt = 12;
// 조도센서 핀
int cds = A1;

// 문 열고 닫을 때의 소리 음계
int ton[]={261,294,330,349,392,440,494,523};

// 문이 닫히기 이전과 보안단계 실패시 소리 음계
int clton[] = {494, 294, 494, 294};

// 라즈베리파이로부터 전송된 데이터 저장
char ser;

// Open the Door
void open_func(){
  // Motor Control
  digitalWrite(green,HIGH);
  digitalWrite(red,LOW);
  
  // Opening sound
  for(int i=0;i<8;i++){
    tone(piz,ton[i]);
    delay(250);
  }
  noTone(piz);
}

// Close the Door
void close_func(){
  // Motor Control
  digitalWrite(green, LOW);
  digitalWrite(red,HIGH);
}


void setup(){
 Serial.begin(9600);
 pinMode(green, OUTPUT);
 pinMode(red,OUTPUT);
 pinMode(piz,OUTPUT); // piezo buzzer
 pinMode(swt,INPUT_PULLUP); //switch
}

void loop(){
  // 아날로그 핀으로부터 조도 센서 값 read
  int cdsval = analogRead(cds);
  Serial.println(digitalRead(swt)); // switch read
  
  // Raspberry Pi에서 데이터 전송 되었을 경우
  while(Serial.available()){
    // 데이터 read
    ser = Serial.read();
    
    // 도어락의 보안 단계 성공시 문 열림
    if(ser == '1'){
      open_func();
    }
    //보안단계 실패시(ser에 '0'이 전송됨) 문이 안열리고 짧은 소리가 남
    else{
      close_func();

      for(int i=0;i<4;i++){
       tone(piz,clton[i]);
       delay(200);
      }
      noTone(piz);
    }
  }
  
  // switch가 눌렸을 경우 - 집 안에서 밖으로 문열고 나가는 상황
  if(digitalRead(swt)==LOW){
    // 스위치 눌렀을 때 문이 열려있는 경우 문을 닫고 닫혀있으면 열기
    // ser이 1이면 문이 열려 있으므로 닫고 ser=0 로 변경
    if(ser == '1'){
      close_func();
      for(int i=7;i>=0;i--){
         tone(piz,ton[i]);
         delay(250);
      }
      noTone(piz); 
      ser = '0';
    }
    // ser=0 이면 문이 닫혀 있으므로 열고 ser=1 로 변경
    else{
      open_func();
      ser = '1';
    }
   }
   
   // 문이 닫힌 후 자동으로 도어락이 잠기는 상황
   // 도어락이 열려있고(ser = 1) 어두워졌으면(조도센서 값 600 초과) 도어락을 잠금
   if(cdsval > 600 && ser== '1'){
     // 문이 닫힌 후 바로 도어락이 잠기지 않도록 delay
     delay(500);
     
     // 도어락이 잠기기 전 또는 라즈베리파이에서 보안단계 실패 시 나는 소리
     for(int i=3;i>=0;i--){
       tone(piz,clton[i]);
       delay(200);
     }
     noTone(piz);

     delay(400);
     close_func();
     
     // 도어락이 잠길 때 나는 소리
     for(int i=7;i>=0;i--){
         tone(piz,ton[i]);
         delay(250);
     }
     noTone(piz); 
     delay(800);
     
     // 도어락이 닫혔으므로 set = 0 으로 변경
     ser = '0';
   }

}