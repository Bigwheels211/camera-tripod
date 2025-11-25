import gpiozero
import threading
import time
tiltMotorForwardPin = 0
tiltMotorBackwardPin = 0
tiltMotorActivatePin = 0
rotationMotorForwardPin = 0
rotationMotorBackwardPin = 0
rotationMotorActivatePin = 0

class motorController:
    tiltMotor = Motor(tiltMotorForwardPin, tiltMotorBackwardPin, tiltMotorActivatePin)
    rotationMotor = Motor(rotationMotorForwardPin, rotationMotorBackwardPin, rotationMotorActivatePin)
    def moveX(xVector):
        if (xVector < 0):
            rotationMotor.reverse()
            sleep(0.03)
            rotationMotor.stop()
        if (xVector > 0):
            rotationMotor.forward()
            sleep(0.03)
            rotationMotor.stop()
    def moveY(yVector):
        if (yVector < 0):
            tiltMotor.reverse()
            sleep(0.03)
            tiltMotor.stop()
        if (yVector > 0):
            tiltMotor.forward()
            sleep(0.03)
            tiltMotor.stop()
    def move(xVector, yVector):
        moveX(xVector)
        moveY(yVector)