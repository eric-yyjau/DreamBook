import RPi.GPIO as IO
from time import sleep
import time
import _thread

# page_action = []
# detectPage = False

# def ReadSensor(thread_name, detectPage, page_action):
def ReadSensor(thread_name, det, pg):

    global page_action, detectPage
    IO.setmode(IO.BCM)
    IO.setup(12,IO.IN)
    IO.setup(19, IO.IN)
    prev = "temp"
    prev_ts = time.time()

    state = "start"
    A_val = "temp"
    A_ts = 0
    B_val = "temp"
    start_ts = 0
    while True:
        isLeft = IO.input(12)
        isRight = IO.input(19)
        if state == "hit_two" or state == "start":
            if not (isLeft or isRight):
                continue
            if (B_val == "left" and isRight) or (B_val == "right" and isLeft) or (A_val == "temp" and B_val == "temp"):
                state = "hit_one"
                
                if isLeft:
                    A_val = "left"
                if isRight:
                    A_val = "right"
                print ("going to state 1", A_val, B_val)
                start_ts = time.time()
            
            

        if state == "hit_one" and detectPage :
            if time.time()-start_ts > 2.0:
                state = "hit_two"
                A_val = "temp"
                B_val = "temp"
                print ("time exceeded", A_val, B_val)
            if not (isLeft or isRight):
                continue
            if (A_val == "left" and isRight) or (A_val == "right" and isLeft):
                
                state = "hit_two"
                if isLeft:
                    B_val = "left"
                if isRight:
                    B_val = "right"
                if A_val == "left" and B_val == "right":
                    print ("front flip", A_val, B_val)
                    page_action.append(1)
                    while True:
                        if not (IO.input(12) or IO.input(19)):
                            time.sleep(0.1)
                            if not (IO.input(12) or IO.input(19)):
                                break
                    A_val = "temp"
                    B_val = "temp"

                if A_val == "right" and B_val == "left":
                    print ("back flip", A_val, B_val)
                    page_action.append(-1)
                    while True:
                        if not (IO.input(12) or IO.input(19)):
                            time.sleep(0.1)
                            if not (IO.input(12) or IO.input(19)):
                                break
                    A_val = "temp"
                    B_val = "temp"
                print ("going to state 2", A_val, B_val)
            else:
                pass

        sleep(0.01)

if __name__=="__main__":
    page_action = []
    detectPage = False
    _thread.start_new_thread( ReadSensor, ("Thread-1",detectPage,page_action))
    while True:
        time.sleep(2)
        print("2 seconds")


