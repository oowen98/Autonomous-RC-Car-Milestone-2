/* 
This Arduino Program will only read the PWM Input signals from Channel 1 and 2 of the receiver and send it to the Raspberry Pi.
*/

#include <Wire.h>

#define mux_select 5
#define ch1_steering 3
#define ch2_throttle 2


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

  Serial.print("Steering PWM: ");
  Serial.print(ch1_steering_PWM_input);
  Serial.print(" Throttle PWM: ");
  Serial.println(ch2_throttle_PWM_input);

}
