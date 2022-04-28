import pigpio
from time import sleep
from keyboardInterupt import KeyboardInterupt
import webcam

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
    while self._running:
      char = self.keyint.getch()
      keep_running, key = self.keyint.keyInput(char)

      # ~ self.move_servos_full_return(key)
      self.move_servos_manual(key)
      
      if(not keep_running):
        self.terminate()
      
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
    
# ~ sc = ServoControl()
# ~ sc.run()
