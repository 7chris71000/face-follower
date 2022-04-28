import numpy as np
import cv2
import time
import math
#import ipdb

class Webcam:
  
  def __init__(self):
    # VideoCapture param is the device index
    # To use an existing video file use, cv2.VideoCapture('filename.mp4')
    print('Init webcam')
    self.capture = cv2.VideoCapture(0)
    self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  
  def start_video(self):
    print('Start capture...')

    #fps = self.capture.get(cv2.CAP_PROP_FPS)
    #print("Frames per second using self.capture.get(cv2.CAP_PROP_FPS): {0}".format(fps))
    
    # Number of frames to capture
    num_frames = 100;
    #print("Capturing {0} frames".format(num_frames))

    # Start time
    #start = time.time()

    i = 0
    while(i < num_frames):
      # Capture frame-by-frame
      frame_read_success, frame = self.capture.read()

      # Display the resulting frame
      if frame_read_success:
        # change to appear as front camera
        frame = cv2.rotate(frame, 0)
        frame = cv2.rotate(frame, 0)
        frame = cv2.flip(frame, 0)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        Webcam.find_faces(self, frame, gray)

        cv2.imshow('', frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
          break
          Webcam.end_video(self)
      
      # uncomment if you need it to measure frames
      #i += 1

    # End time
    #end = time.time()

    # Time elapsed
    #seconds = end - start
    #print("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    #fps  = num_frames / seconds;
    #print("Estimated frames per second : {0}".format(fps))
    # ~ Webcam.end_video(self)

  def end_video(self):
    # When everything done, release the capture
    print('Exiting camera...')
    self.capture.release()
    cv2.destroyAllWindows()

  def find_faces(self, frame, grayScale=None):
    # loop through each frame and find the faces in the 'image'
    # Display a square around each face
    if grayScale is not None:
      color = grayScale
    else:
      color = frame
    
    faces = self.face_cascade.detectMultiScale(color, 1.1, 5)
    for(x, y, w, h) in faces:
      # when it has multiple boxes, 
      # find the largest one and establish that as the face
      
      x_middle = math.floor(x+w/2)
      y_middle = math.floor(y+h/2)
      cv2.line(frame, (x_middle, y_middle), (x_middle+1, y_middle+1), (0, 255, 0), 5)
      # cv2.circle(frame, (x_middle, y_middle), math.floor(w/2), (0, 0, 255), 5)
      # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

      # cv2.putText(frame,
                  # 'x:' + str(x_middle) + ' y:' + str(y_middle),
                  # (x_middle, y_middle), 
                  # cv2.FONT_HERSHEY_PLAIN,
                  # 2,
                  # (255, 255, 255),
                  # 2,
                  # cv2.LINE_AA)
