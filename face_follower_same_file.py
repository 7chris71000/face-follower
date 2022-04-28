from threading import Thread
from keyboardInterupt import KeyboardInterupt
from time import sleep
import pigpio
import numpy as np
import cv2
import time
import math

faceData = [0, 0, [0, 0, 0, 0]] # structure: [x middle, y middle, bounding box [top, right, bottom, left]]

class ServoControl:

  def __init__(self):
    print("Init servo's")
    self._running = True
    
    self.pi = pigpio.pi()
    
    self.x_coord = 1500
    self.y_coord = 1500
    
    self.keyint = KeyboardInterupt()
  
  def terminate(self):
    self.reset()
    self._running = False
    print("Terminated servo's")
  
  def run(self):
    print("Servo's listening...")
    
    global faceData
    while self._running:
      x_middle = faceData[0]
      y_middle = faceData[1]
      top = faceData[2][0]
      right = faceData[2][1]
      bottom = faceData[2][2]
      left = faceData[2][3]
      if((top < x_middle < bottom) and (left < y_middle < right)):
        in_frame_message = 'Safe Zone'
      else:
        in_frame_message = 'Out Of Safe Zone'
      print(in_frame_message)
      
      sleep(0.5)
      
      # ~ char = self.keyint.getch()
      # ~ keep_running, key = self.keyint.keyInput(char)

      # ~ self.move_servos_manual(key)
      
      # ~ if(not keep_running):
        # ~ self.terminate()
      
  def move_servos_manual(self, key):
    if(not self.check_for_safe_rotation(key)):      
      if(key == 'a'):
        self.x_coord += 100
        self.pi.set_servo_pulsewidth(17, self.x_coord)
        sleep(0.1)
      elif (key == 'd'):
        self.x_coord -= 100
        self.pi.set_servo_pulsewidth(17, self.x_coord)
        sleep(0.1)
      elif (key == 'w'):
        self.y_coord += 100
        self.pi.set_servo_pulsewidth(18, self.y_coord)
        sleep(0.1)
      elif (key == 's'):
        self.y_coord -= 100
        self.pi.set_servo_pulsewidth(18, self.y_coord)
        sleep(0.1)
  
  def move_servos_full_return(self, key):
    if(key == 'a'):
      print("max x")
      self.pi.set_servo_pulsewidth(17, 2000)
      sleep(0.1)
    elif (key == 'd'):
      print("min x")
      self.pi.set_servo_pulsewidth(17, 1000)
      sleep(0.1)
    elif (key == 'w'):
      print("max y")
      self.pi.set_servo_pulsewidth(18, 2000)
      sleep(0.1)
    elif (key == 's'):
      print("min y")
      self.pi.set_servo_pulsewidth(18, 1000)
      sleep(0.1)
      
    print("mid")
    self.reset()
    sleep(0.1)
    
  def check_for_safe_rotation(self, key):
    if( 
        (key == 'a' and not (1000 <= self.x_coord + 100 <= 2000)) or
        (key == 'd' and not (1000 <= self.x_coord - 100 <= 2000)) or
        (key == 'w' and not (1000 <= self.y_coord + 100 <= 2000)) or
        (key == 's' and not (1000 <= self.y_coord - 100 <= 2000))
      ):
      self.reset()
      return True
    return False

  def reset(self):
    self.pi.set_servo_pulsewidth(17, 1500)
    sleep(0.5)
    self.x_coord = 1500
    
    self.pi.set_servo_pulsewidth(18, 1500)
    sleep(0.5)
    self.y_coord = 1500

class Webcam:
  
  def __init__(self):
    # VideoCapture param is the device index
    # To use an existing video file use, cv2.VideoCapture('filename.mp4')
    print('Init webcam')
    self.capture = cv2.VideoCapture(0)
    self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  
  def start_video(self):
    print('Start capture...')
    while(True):
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
    global faceData
    
    i = 0
    # Set values of rectangle box
    top_left_x = 150
    top_left_y = 150
    bottom_right_x = int(self.capture.get(3)) - 150
    bottom_right_y = int(self.capture.get(4)) - 150
    for(x, y, w, h) in faces:
      # when it has multiple boxes,
      # find the largest one and establish that as the face
      if not i:
        x_middle = math.floor(x+w/2)
        y_middle = math.floor(y+h/2)
        
        cv2.line(frame, (x_middle, y_middle), (x_middle+1, y_middle+1), (0, 255, 0), 5)
        # rectangle to see when user is nearing out of frame
        # Set colour of box
        colour = (0, 0, 255)
        if ((top_left_x < x_middle < bottom_right_x) and (top_left_y < y_middle < bottom_right_y)):
          # set colour of rectangle when the user is out of screen but a face is still recognized
          colour = (0, 255, 0)

        cv2.rectangle(frame, 
                     (top_left_x, top_left_y),
                     (bottom_right_x, bottom_right_y),
                     colour, 1)

        faceData = [x_middle, y_middle, [top_left_x, bottom_right_y, bottom_right_x, top_left_y]] 

      i += 1

cam = Webcam()
CamThread = Thread(target=cam.start_video)
CamThread.start()

servo_control = ServoControl()
ServoThread = Thread(target=servo_control.run)
ServoThread.start()
