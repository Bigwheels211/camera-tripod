from flask import config
import yaml
import cv2
import os
import threading

class camera:
    def __init__(self):
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        self.settings = config['settings']
        self.frame = None
        self.cameraType = self.settings['camera_type']
        if self.cameraType == 'picamera2' or self.cameraType == 'picamera3':
            from picamera2 import Picamera2
            self.picam2 = Picamera2()
            picamera2config = self.picam2.create_video_configuration( 
                                                        main={"size": (1296, 972),
                                                              'format': 'RGB888'},
                                                        sensor={
                                                            'output_size': (1296, 972)})
            self.picam2.configure(picamera2config)
            print('picamera2 started!')
            self.picam2.start()
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()
        elif self.cameraType == 'usb':
            self.usbCam = cv2.VideoCapture(0)
    def _update(self):
        while True:
            if self.cameraType == 'picamera2' or self.cameraType == 'picamera3':
                self.frame = self.picam2.capture_array()
            elif self.cameraType == 'usb':
                isRead, frame = self.usbCam.read()
                if isRead:
                    self.frame = frame
                else:
                    print('Camera not configured properly error')

    def getPixelArray(self):
        return self.frame
    def getJPEG(self):
        ret, jpeg = cv2.imencode('.jpg', self.getPixelArray())
        return jpeg.tobytes()
    def saveJPEG(self):
        image = self.getPixelArray()
        filepath = os.path.join('static', 'bufferimage.jpeg')
        cv2.imwrite(filepath, image)
    def getCenterPoint(self):
        frame = self.getPixelArray()
        image_height, image_width = frame.shape[:2] # Get the width and height of the total image
        return (image_width//2, image_height//2)
    def getPort(self):
        return self.settings['port']
cam = camera()