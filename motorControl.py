from gpiozero import Motor, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import threading
import time
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
pins = config['pins']
Device.pin_factory = PiGPIOFactory()

class motorController:
    tiltMotor = Motor(pins['tiltMotorForward'], pins['tiltMotorReverse'])
    rotationMotor = Motor(pins['rotationMotorForward'], pins['rotationMotorReverse'])
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