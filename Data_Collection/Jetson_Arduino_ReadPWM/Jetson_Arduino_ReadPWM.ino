/* 
This Arduino Program will only read the PWM Input signals from Channel 1 and 2 of the receiver and send it to the Raspberry Pi.
*/

#include <Wire.h>

#define mux_select 5
#define ch1_steering 3
#define ch2_throttle 2

int i2c_Address_Arduino = 0x40; //Arduino i2c Address
//unsigned int data[10] = {0};

byte ThrottleSteeringPWM[4] = {0};

int ch1_steering_PWM_input = 0;
int ch2_throttle_PWM_input = 0;

int steering_prev_time = 0;
int throttle_prev_time = 0;

void setup() {
  // put your setup code here, to run once:

  pinMode(mux_select, OUTPUT);

  //External Interrupt setup to read pwm values for throttle and steering
  attachInterrupt(digitalPinToInterrupt(ch1_steering), steering_rising, RISING);
  attachInterrupt(digitalPinToInterrupt(ch2_throttle), throttle_rising, RISING);

  Serial.begin(9600);
  while(!Serial){} 

  //i2c Setup
  Wire.begin(i2c_Address_Arduino);
  Wire.onRequest(sendData);
}

void sendData(){
  Wire.write(ThrottleSteeringPWM, 4);
}


void steering_rising(){
  attachInterrupt(digitalPinToInterrupt(ch1_steering), steering_falling, FALLING);
  steering_prev_time = micros();
}

void steering_falling(){
  attachInterrupt(digitalPinToInterrupt(ch1_steering), steering_rising, RISING);
  ch1_steering_PWM_input = micros() - steering_prev_time;
}

void throttle_rising(){
  attachInterrupt(digitalPinToInterrupt(ch2_throttle), throttle_falling, FALLING);
  throttle_prev_time = micros();
}

void throttle_falling() {
  attachInterrupt(digitalPinToInterrupt(ch2_throttle), throttle_rising, RISING);
  ch2_throttle_PWM_input = micros() - throttle_prev_time;
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(mux_select, HIGH); //Continuously output HIGH to the multiplexer for transmitter control

  ThrottleSteeringPWM[0] = highByte(ch2_throttle_PWM_input); //PWM Values will be around 900 - 2000, so we will send 2 bytes to Raspberry Pi
  ThrottleSteeringPWM[1] = lowByte(ch2_throttle_PWM_input);

  ThrottleSteeringPWM[2] = highByte(ch1_steering_PWM_input); //Upper 8 bits
  ThrottleSteeringPWM[3] = lowByte(ch1_steering_PWM_input); //Lower 8 bits
  
  Serial.print("Steering PWM: ");
  Serial.print(ch1_steering_PWM_input);
  Serial.print(" Throttle PWM: ");
  Serial.print(ch2_throttle_PWM_input);

  Serial.print(" Steering Bytes: ");
  Serial.print(ThrottleSteeringPWM[2]);
  Serial.print("_");
  Serial.print(ThrottleSteeringPWM[3]);
  
  Serial.print(" Throttle Bytes: ");
  Serial.print(ThrottleSteeringPWM[0]);
  Serial.print("_");
  Serial.println(ThrottleSteeringPWM[1]);


}
