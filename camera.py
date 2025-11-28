import yaml
import cv2
import os
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

settings = config['settings']
cameraType = settings['camera_type']
if cameraType == 'picamera2':
    from picamera2 import Picamera2
    picam2 = Picamera2()
    picamera2config = picam2.create_video_configuration( 
                                                        main={"size": (1920, 1080),
                                                              'format': 'RGB888'},
                                                        sensor={
                                                            'output_size': (1920, 1080)})
    picam2.configure(picamera2config)
    print('picamera2 started!')
    picam2.start()
elif cameraType == 'usb':
    usbCam = cv2.VideoCapture(0)
def getPixelArray():
    if cameraType == 'picamera2':
        return picam2.capture_array()
    elif cameraType == 'usb':
        isRead, frame = usbCam.read()
        if isRead:
            return frame
        else:
            return None
    else:
        print('Camera not configured properly error')
def getJPEG():
    ret, jpeg = cv2.imencode('.jpg', getPixelArray())
    return jpeg.tobytes()
def saveJPEG():
    image = getPixelArray()
    filepath = os.path.join('static', 'bufferimage.jpeg')
    cv2.imwrite(filepath, image)
def getCenterPoint():
    frame = getPixelArray()
    image_height, image_width = frame.shape[:2] # Get the width and height of the total image
    return (image_width//2, image_height//2)
def getPort():
    return settings['port']