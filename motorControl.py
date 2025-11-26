from gpiozero import Motor, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import threading
import time

Device.pin_factory = PiGPIOFactory()
tiltMotorForwardPin = 12
tiltMotorBackwardPin = 13
rotationMotorForwardPin = 18
rotationMotorBackwardPin = 19

class motorController:
    tiltMotor = Motor(tiltMotorForwardPin, tiltMotorBackwardPin)
    rotationMotor = Motor(rotationMotorForwardPin, rotationMotorBackwardPin)
    def moveX(self, xVector):
        if (xVector < 0):
            self.rotationMotor.reverse()
            time.sleep(0.03)
            self.rotationMotor.stop()
        if (xVector > 0):
            self.rotationMotor.forward()
            time.sleep(0.03)
            self.rotationMotor.stop()
    def moveY(self,yVector):
        if (yVector < 0):
            self.tiltMotor.reverse()
            time.sleep(0.03)
            self.tiltMotor.stop()
        if (yVector > 0):
            self.tiltMotor.forward()
            time.sleep(0.03)
            self.tiltMotor.stop()
    def move(self, xVector, yVector):
        self.moveX(xVector)
        self.moveY(yVector)