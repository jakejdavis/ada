### BASED UPON PICOCON motorTest02.py ###
## http://4tronix.co.uk/initio/motorTest2.py ##
import picocon # Import picocon
import time # Import other modules
import sys 
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows


speed = 60 # Set defualt speed

print("Tests the motors by using the arrow keys to control")
print("Use , or m to slow down")
print("Use . or n to speed up")
print("Speed changes take effect when the next arrow key is pressed")
print("Press Ctrl-C to end")
print()

picocon.init() # Initilize picocon 

try: # Try 
    while True: # While forever
        keyp = readkey() # Get keypress 
        if keyp == 'w' or ord(keyp) == 16: # If keypress is up arrow or w
            picocon.forward(speed) # Set motors to forward
            print('Forward', speed) # Print "Forward" followed by the speed
        elif keyp == 'z' or ord(keyp) == 17: # If keypress is down arrow or z
            picocon.reverse(speed) # Set motors to reverse
            print('Reverse', speed) # Print "Reverse" followed by the speed
        elif keyp == 's' or ord(keyp) == 18: # If keypress is right arrow or s
            picocon.spinRight(speed) # Set motors to spin right
            print('Spin Right', speed) # Print "Spin Right" followed by speed
        elif keyp == 'a' or ord(keyp) == 19: # If keypress is left arrow or a
            picocon.spinLeft(speed) # Set motors to spin left
            print('Spin Left', speed) # Print "Spin Left" followed by speed
        elif keyp == '.' or keyp == 'n': # If keypress is '.' or 'n'
            speed = min(100, speed+10) # If speed less than 100, add 10
            print('Speed+', speed) # Print "Speed+" followed by the new speed
        elif keyp == ',' or keyp == 'm': # If keypress is ',' or 'm'
            speed = max (0, speed-10) # If speed is more than 0, subtract 10
            print('Speed-', speed) # Print "Speed+" followed by the new speed
        elif keyp == ' ': # If the keypress a space
            picocon.stop() # Stop the motors
            print('Stop') # Print "Stop"
        elif ord(keyp) == 3: 
            break

except KeyboardInterrupt: # If Ctrl-C pressed
    print() # Print new line & exit

finally:
    picocon.cleanup()
    
