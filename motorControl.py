from adafruit_servokit import ServoKit
import camera
import numpy as np
import cv2
import threading
import time
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
pins = config['channels']
inverted = config['inverted']
holdValues = config['holdValues']
kit = ServoKit(channels=16)
class motorController:
    
    def __init__(self):
        self.rotationMotor = kit.continuous_servo[pins['rotationMotor']]
        self.tiltMotor = kit.continuous_servo[pins['tiltMotor']]
        if inverted['rotationMotor']:
            self.rotationMotorScale = -1
        else:
            self.rotationMotorScale = 1
        if inverted['tiltMotor']:
            self.tiltMotorScale = -1
        else:
            self.tiltMotorScale = 1
        self.rotationMotorHoldValue = holdValues['rotationMotor']
        self.tiltMotorHoldValue = holdValues['tiltMotor']
        self.rotationCalibrationFactor = 0 # Seconds/pixel
        self.tiltCalibrationFactor = 0 # Seconds/pixel
        print("Initializing motors...")
        self.rotationMotor.throttle = 0.1
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
        if (xVector < -10):
            self.rotationMotor.throttle = 1.0*self.rotationMotorScale
        elif (xVector > 10):
            self.rotationMotor.throttle = -1.0*self.rotationMotorScale
        else:
            self.rotationMotor.throttle = self.rotationMotorHoldValue
    def moveY(self,yVector):
        if (yVector < -10):
            self.tiltMotor.throttle = -1.0*self.tiltMotorScale
        elif (yVector > 10):
            self.tiltMotor.throttle = 1.0*self.tiltMotorScale
        else:
            self.tiltMotor.throttle = self.tiltMotorHoldValue
    def move(self, xVector, yVector):
        self.moveX(xVector)
        self.moveY(yVector)
    def stop(self):
        self.rotationMotor.throttle = self.rotationMotorHoldValue
        self.tiltMotor.throttle = self.tiltMotorHoldValue