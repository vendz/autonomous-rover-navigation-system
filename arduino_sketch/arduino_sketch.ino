
// This code receives commands from TiHAN onboard computer to control
// the rover motors (attached to Cytron board) 

#include "CytronMotorDriver.h"



Servo myservo1 , myservo2;  // create servo object to control a servo
// twelve servo objects can be created on most boards
int pos = 0;    // variable to store the servo position



// Create two motor objects.
CytronMD motor1(PWM_DIR, 5, 4); // Internal Circuit.
CytronMD motor2(PWM_DIR, 6, 7); // Internal Circuit.


void setup() 
{
  Serial.begin(9600); 
  pinMode(10, INPUT); // Set digital pin 11 as an input.
  pinMode(11, INPUT); // Set digital pin 10 as an input.  
}

void loop() 
{ 
  // Check if there is data available to read from the serial port
  if (Serial.available()) 
  {
   // Read the command from the serial port- to receive motor control codes
    String command = Serial.readStringUntil('\n');
    Serial.println(command);

    if(command == "0"){
      motor1.setSpeed(0);
      motor2.setSpeed(0);
    }

    if(command == "1"){
      motor1.setSpeed(100);
      motor2.setSpeed(100);
    }

    if(command == "-2"){
      motor1.setSpeed(-150);
      motor2.setSpeed(150);
    }

    if(command == "2"){
      motor1.setSpeed(150);
      motor2.setSpeed(-150);
    }
    

    // Read the command from the serial port- to receive pan-tilt control codes
    // String command2 = Serial.readStringUntil('\n');
    // Serial.println(command2);
    
    // // Process the command to set motor speeds
    // if (command.startsWith("L") && command.indexOf('R') != -1) 
    // {
    //   // Extract the left and right motor speeds from the command
    //   int command_code = command.substring(1, command.indexOf('R')).toInt();
    //   Serial.println(command_code);
    //   //int right_speed = command.substring(command.indexOf('R') + 1).toInt();


    //   if (command_code == 1)
    //   {
    //     //Forward
        
    //     motor1.setSpeed(100);
    //     motor2.setSpeed(100);
    //   }

    //     if (command_code == -1)
    //     {
    //     //Reverse
     
    //     motor1.setSpeed(-100);
    //     motor2.setSpeed(-100);
    //     }

        
    //     if (command_code == 0) 
    //     {
    //     //Stop
        
    //     motor1.setSpeed(0);
    //     motor2.setSpeed(0);
    //     }

        
    //     if (command_code == 2)
    //     {
    //     //Right-turn
        
    //     motor1.setSpeed(150);
    //     motor2.setSpeed(-150);
    //     }
        
    //     if (command_code == -2)
    //     {
    //     //Left-turn
        
    //     motor1.setSpeed(-150);
    //     motor2.setSpeed(150);
    //     }      
    // }
    
  }    


}
