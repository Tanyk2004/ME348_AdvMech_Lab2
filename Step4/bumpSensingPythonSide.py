#!/usr/bin/env python3
import serial
import time
import numpy as np
import enum

from sendStringScript import sendString
leftMotor=int(0)
rightMotor=int(0)

bumpSensors = [1, 1, 1, 1, 1, 1]

class States(enum.Enum):
    STOP = 0
    AVOID_LEFT = 1
    AVOID_RIGHT = 2
    AVOID_HEADON = 3
    GO = 4

currentState = States.STOP

def avoid_right():
    global leftMotor
    global rightMotor
    leftMotor = -50
    rightMotor = -50

    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
    time.sleep(0.5) 
    leftMotor = -50
    rightMotor = 50
    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
    time.sleep(0.5) 
    currentState = States.GO

def avoid_left():
    global leftMotor
    global rightMotor
    leftMotor = -50
    rightMotor = -50
    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
    time.sleep(0.5) 
    leftMotor = 50
    rightMotor = -50
    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
    time.sleep(0.5) 
    currentState = States.GO

def avoid_headon():
    global leftMotor
    global rightMotor
    leftMotor = -50
    rightMotor = -50

    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
    time.sleep(0.5) 
    leftMotor = 50
    rightMotor = -50

    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
    time.sleep(0.5) 
    leftMotor = 50
    rightMotor = 50

    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
    time.sleep(0.5)
    leftMotor = 50
    rightMotor = -50
    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
    time.sleep(0.5)
    currentState = States.GO


def go():
    global leftMotor
    global rightMotor
    leftMotor = 100
    rightMotor = 100

    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)

def stop():
    leftMotor = 0
    rightMotor = 0

    sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)

if __name__ == '__main__':
    ser=serial.Serial('/dev/ttyACM0',115200)
    #every time the serial port is opened, the arduino program will restart, very convient!
    ser.reset_input_buffer()
    ready = 0
    

    while True:
        print("Sending: ", '<'+str(leftMotor)+','+str(rightMotor)+'>')
        #think of the below line as the default condition where no pairs of sensors are triggered as state 0, where the robot moves forward
        sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
        #ser.write(b'<'+bytes(str(leftMotor),'utf-8')+b','+bytes(str(rightMotor),'utf-8')+b'>')


        #why so I append '<' and '>' to the beginning and end of my message that I send to the arduino?

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8')
            print(line)
            line = line.strip()
                #ive just called 2 methods from the ser object, what do they do? read the documentation and find out!
            # line=line.split(',')
                #this one i wont ask you about this one is pretty self explanitory

            try:
                    
                bumpSensors[0]=int(line[0])
                bumpSensors[1]=int(line[1])
                bumpSensors[2]=int(line[2])

                bumpSensors[3]=int(line[3])  
                bumpSensors[4]=int(line[4])
                bumpSensors[5]=int(line[5])

                print(bumpSensors)
                
            except Exception as e:
                print("packetLost", e) 
                continue
                #why do I have this exepction? 
        if (len(bumpSensors) == 0):
            continue
        # sendString('/dev/ttyACM0',115200,'<'+str(-leftMotor)+','+str(-rightMotor)+'>',0.0005)
        #rudimentery state machine
        if bumpSensors[0] < 1 and bumpSensors[1] < 1:
            currentState = States.AVOID_RIGHT
        elif bumpSensors[2] < 1 and bumpSensors[3] < 1:
            currentState = States.AVOID_HEADON
        elif bumpSensors[4] < 1 and bumpSensors[5] < 1:
            currentState = States.AVOID_LEFT
        else:
            currentState = States.GO
        print("Current State: ", currentState) 
        match currentState:
            case States.AVOID_RIGHT:
                avoid_right()
            case States.AVOID_LEFT:
                avoid_left()
            case States.AVOID_HEADON:
                avoid_headon()
            case States.GO:
                go() 
            case _:
                stop()
        

