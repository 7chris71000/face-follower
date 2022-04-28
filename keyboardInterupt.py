import time
import sys
import tty
import termios
# Function to capture keyboard input

class KeyboardInterupt:
    def __init__(self):
        print("KeyboardInterupt starting")
    
    def run(self):
        keep_running = True
        while keep_running:
            char = self.getch()
            keep_running = self.keyInput(char)
        exit()
            
    
    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    def keyInput(self, char):
        # Exits Program
        if char == "q":
            print("Exiting...")
            return False, char
        return True, char

# ~ keyint = KeyboardInterupt()

# ~ while True:
    # ~ # capture keyboard input
    # ~ char = keyint.getch()
    # ~ keyint.keyInput(char)
