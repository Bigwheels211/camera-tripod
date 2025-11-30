from gpiozero import Motor, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import camera
import numpy as np
import cv2
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
    def __init__(self):
        self.rotationCalibrationFactor = 0 # Seconds/pixel
        self.tiltCalibrationFactor = 0 # Seconds/pixel
        self.calibrate()
    def calibrateRotation(self):
        img1 = camera.getPixelArray()
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img1 = img1.astype('float32')
        self.rotationMotor.forward()
        time.sleep(0.5)
        self.rotationMotor.stop()
        img2 = camera.getPixelArray()
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        img2 = img2.astype('float32')
        shift = cv2.phaseCorrelate(img1, img2)
        self.rotationCalibrationFactor = 0.5 / shift[0][0]
        print("Rotation calibration factor:", self.rotationCalibrationFactor)
    def calibrateTilt(self):
        img1 = camera.getPixelArray()
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img1 = img1.astype('float32')
        self.tiltMotor.forward()
        time.sleep(0.5)
        self.tiltMotor.stop()
        img2 = camera.getPixelArray()
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        img2 = img2.astype('float32')
        shift = cv2.phaseCorrelate(img1, img2)
        self.tiltCalibrationFactor = 0.5 / shift[0][1]
        print("Tilt calibration factor:", self.tiltCalibrationFactor)
    def calibrate(self):
        self.calibrateRotation()
        self.calibrateTilt()
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