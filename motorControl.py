from gpiozero import Motor, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from adafruit_servokit import ServoKit
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
kit = ServoKit(channels=16)
class motorController:
    
    def __init__(self):
        self.rotationMotor = kit.continuous_servo[12]
        self.tiltMotor = kit.continuous_servo[13]
        self.rotationCalibrationFactor = 0 # Seconds/pixel
        self.tiltCalibrationFactor = 0 # Seconds/pixel
        print("Initializing motors...")
        self.rotationMotor.throttle = 0.1
        #self.calibrate()
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
            self.rotationMotor.throttle = 1.0
            time.sleep(0.03)
            self.rotationMotor.throttle = 0.1
        if (xVector > 0):
            self.rotationMotor.throttle = -1.0
            time.sleep(0.03)
            self.rotationMotor.throttle = 0.1
    def moveY(self,yVector):
        if (yVector < 0):
            self.tiltMotor.throttle = -1.0
            #time.sleep(0.03)
            #self.tiltMotor.throttle = 0.1
        if (yVector > 0):
            self.tiltMotor.throttle = 1.0
            #time.sleep(0.03)
            #self.tiltMotor.throttle = 0.1
    def move(self, xVector, yVector):
        self.moveX(xVector)
        self.moveY(yVector)
    def stop(self):
        self.rotationMotor.throttle = 0.09
        self.tiltMotor.throttle = 0.09