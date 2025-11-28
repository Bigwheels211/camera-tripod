import numpy as np
import cv2
import threading
from motorControl import motorController
import camera
import time
import stopwatch

def findCenter(face):
    return (face[0] + face[2]//2, face[1] + face[3]//2)
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") # Initiallized the face_classifier with the haarcascades model

def detect_center_point(vid, prev, numNotFound):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY) # converts the image to grayscale
    scaleFactor = 0.5 # Scale factor for the image to be scaled down for faster processing
    scaled_width = int(gray_image.shape[1] * scaleFactor) # Scales the image down to half size for faster processing
    scaled_height = int(gray_image.shape[0] * scaleFactor)
    small_gray_image = cv2.resize(gray_image, (scaled_width, scaled_height)) # Resizes the image to the new scaled size
    faces = face_classifier.detectMultiScale(small_gray_image, 1.1, 5, minSize=(100, 100)) # Locates the faces and returns them in the format[x,y,w,h]
    if faces is None: # If there is no faces found, return None
        return  None
    closestFace = (0,0,0,0)
    closestDistance = 10000
    currentFace = 0
    multiplier = int(1/scaleFactor) # Multiplier to get the face coordinates back to the original size
    for (x, y, w, h) in faces: # Loops through every face
        faces[currentFace] = (x*multiplier, y*multiplier, w*multiplier, h*multiplier) # Scales the face coordinates back to the original size
        center_point = (x+w//2, y+h//2) # Finds the center point of every face
        if prev is None: # If there is no previous face, just return the first face that is found
            return center_point
        currentDistance = np.abs(prev[0] - center_point[0]) + np.abs(prev[1] - center_point[1]) # add the xVector + yVector to get the total vector
        if numNotFound > 10: #If the face hasn't been found in 10 frames, return the first face that is found
            cv2.putText(vid,'Resetting face',(0,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
            return center_point
        if currentDistance < closestDistance: # if the currentDistance is closer that the current closestDistance then set the current distance and face as the closest
            closestFace = faces[currentFace]
            closestDistance = currentDistance
        currentFace += 1 # index the current face
    center_point = findCenter(closestFace) #Find the center point of the closest face
    if center_point == (0,0):
        return None
    cv2.circle(vid, center_point, closestFace[2]//2, (0,0,255),4) #Draw a circle around the face
    return center_point # return the center of the closest face to the previous
class FacialTracking:
    def __init__(self):
        self.running = False
        self.thread = None
        self.frame = None
        self.lock = threading.Lock()
        self.controller = motorController()
        
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.thread = None
    def run(self):
        watch = stopwatch.Stopwatch()
        video_frame = camera.getPixelArray()
        prev_center = None # Initializes the prev_center variable, which will be used to tell the distance from faces in the current frame to the face from the previous frame
        counter = 0 # Initializes the counter variable, which will be used to tell how many frames in a row there has been since the face has been found
        window_center = camera.getCenterPoint()
        while self.running:
            watch.start()
            video_frame = camera.getPixelArray() # Read the current frame and set it as video_frame
            if video_frame is None: # If no frame is read, break
                break
            face_center = detect_center_point(video_frame, prev_center, counter) #Find the center point of the face that is closest to the previous
            if face_center is None: # If no face is found, index the counter variable, write no face found, and set the currrent face equal to the face in the last frame
                counter = counter + 1
                cv2.putText(video_frame,'No face found',(0,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
                face_center = prev_center
            else: # If a face is found, reset the counter variable
                counter = 0
            prev_center = face_center # Set the previous frame equal to the current frame for use in the next iteration of the loop
            if face_center is not None: # If a face_center is found, find the vectors from that face to the center of the camera and put them on the video loop at the center of the face
                xVector = face_center[0] - window_center[0]
                yVector = window_center[1] - face_center[1]
                total_vector = str(xVector) + ', ' + str(yVector)
                cv2.putText(video_frame,total_vector,face_center,cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
                #self.controller.move(xVector,yVector)
            with self.lock:
                self.frame = video_frame.copy()
            watch.get_elapsed_time()
            watch.reset()
        else:
            print("Cannot Read Video")
    def get_frame_jpeg(self):
        with self.lock:
            if self.frame is None:
                return None
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            return jpeg.tobytes()