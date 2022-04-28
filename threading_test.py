from threading import Thread
import time

from keyboardInterupt import KeyboardInterupt


global global_cycle
global_cycle = 0.0

class ThreadingTest1:
	def __init__(self):
		print("Starting thread 1...")
		self._running = True
	
	def terminate(self):
		self._running = False
		print("Terminating thread 1...")	
	
	def run(self):
		global global_cycle
		while self._running:
			time.sleep(5)
			global_cycle = global_cycle + 1.0
			print("5 second thread global_cycle+1.0 -", round(global_cycle,1))
			
class ThreadingTest2:
	def __init__(self):
		print("Starting thread 2...")
		self._running = True
	
	def terminate(self):
		self._running = False
		print("Terminating thread 2...")
	
	def run(self):
		global global_cycle
		while self._running:
			time.sleep(2)
			global_cycle = global_cycle + 2.0
			print("2 second thread global_cycle+2.0 -", round(global_cycle,1))

# ~ #Create class
# ~ FiveSecond = ThreadingTest1()

# ~ #Create thread
# ~ FiveSecondThread = Thread(target=FiveSecond.run)

# ~ #Start thread
# ~ FiveSecondThread.start()

# ~ #Create class
# ~ TwoSecond = ThreadingTest2()

# ~ #Create thread
# ~ TwoSecondThread = Thread(target=TwoSecond.run)

# ~ #Start thread
# ~ TwoSecondThread.start()

# ~ global Exit
# ~ Exit = False

# ~ keyint = KeyboardInterupt()
# ~ while not Exit:
    # ~ # capture keyboard input
    # ~ char = keyint.getch()
    # ~ Exit = keyint.keyInput(char)
    
    # ~ if Exit:
        # ~ FiveSecond.terminate()
        # ~ TwoSecond.terminate()
