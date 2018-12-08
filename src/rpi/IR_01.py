import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(2,IO.OUT) #GPIO 2 -> Red LED as output
IO.setup(3,IO.OUT) #GPIO 3 -> Green LED as output
pin_in = 16
IO.setup(pin_in,IO.IN) #GPIO 14 -> IR sensor as input

while 1:

        if(IO.input(pin_in)==True): #object is far away
            print("Far!") 
        elif(IO.input(pin_in)==False): #object is near
            print("Near!")
        time.sleep(0.3)
