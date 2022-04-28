from threading import Thread
from threading_test import ThreadingTest1
from keyboardInterupt import KeyboardInterupt
from pigpio_servos import ServoControl
from webcam import Webcam

# ~ #Create class
# ~ FiveSecond = ThreadingTest1()
# ~ #Create thread
# ~ FiveSecondThread = Thread(target=FiveSecond.run)
# ~ #Start thread
# ~ FiveSecondThread.start()

cam = Webcam()
CamThread = Thread(target=cam.start_video)
CamThread.start()

servo_control = ServoControl()
ServoThread = Thread(target=servo_control.run)
ServoThread.start()
 
# ~ keyint = KeyboardInterupt()
# ~ KeyIntThread = Thread(target=keyint.run)
# ~ KeyIntThread.start()

# create a global that keeps the input from the user. See if this can be used
