from gpiozero import AngularServo
from time import sleep
from keyboardInterupt import KeyboardInterupt
import webcam

class ServoControl:

  def __init__(self):
    print("Init servo's")
    self._running = True
    self.servo_x = AngularServo(17, min_angle=-50, max_angle=41)
    self.servo_y = AngularServo(18, min_angle=-50, max_angle=41)
    
    self.x_coord = 0
    self.y_coord = 0
    
    self.keyint = KeyboardInterupt()
  
  def terminate(self):
    self.reset()
    self._running = False
    print("Terminated servo's")
  
  def run(self):
    print("Servo's listening...")
    while self._running:
      # ~ if(webcam.facesFound == 1):
        # ~ print(str(webcam.facesFound))
      char = self.keyint.getch()
      keep_running, key = self.keyint.keyInput(char)

      # ~ self.move_servos_full_return(key)
      self.move_servos_manual(key)
      
      if(not keep_running):
        self.terminate()
      
  def move_servos_manual(self, key):
    global facesFound
    print(facesFound)
    if(not self.check_for_safe_rotation(key)):      
      if(key == 'a'):
        self.x_coord += 3
        self.servo_x.angle = self.x_coord
        sleep(0.1)
      elif (key == 'd'):
        self.x_coord -= 3
        self.servo_x.angle = self.x_coord
        sleep(0.1)
      elif (key == 'w'):
        self.y_coord += 3
        self.servo_y.angle = self.y_coord
        sleep(0.1)
      elif (key == 's'):
        self.y_coord -= 3
        self.servo_y.angle = self.y_coord
        sleep(0.1)
  
  def move_servos_full_return(self, key):
    if(key == 'a'):
      print("max x")
      self.servo_x.max()
      sleep(0.1)
    elif (key == 'd'):
      print("min x")
      self.servo_x.min()
      sleep(0.1)
    elif (key == 'w'):
      print("max y")
      self.servo_y.max()
      sleep(0.1)
    elif (key == 's'):
      print("min y")
      self.servo_y.min()
      sleep(0.1)
      
    print("mid")
    self.servo_x.mid()
    self.servo_y.mid()
    sleep(0.1)
    
  def check_for_safe_rotation(self, key):
    if( 
      (key == 'a' and not (-47 <= self.x_coord + 3 <= 39)) or
      (key == 'd' and not (-47 <= self.x_coord - 3 <= 39)) or
      (key == 'w' and not (-47 <= self.y_coord + 3 <= 39)) or
      (key == 's' and not (-47 <= self.y_coord - 3 <= 39))
    ):
      self.reset()
      return True
    return False

  
  def reset(self):
    self.servo_x.mid()
    sleep(0.5)
    self.x_coord = 0
    
    self.servo_y.mid()
    sleep(0.5)
    self.y_coord = 0
    
# ~ sc = ServoControl()
# ~ sc.run()
