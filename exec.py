import time
from ultra import Detector

if __name__ == '__main__':
    try:
        detect = Detector()
        detect.setup()
        flip1 = 0
        flip2 = 0
        flip3 = 0
        while True:
            flip1 = flip2
            flip2 = flip3
            flip3 = detect.getReading()
            if flip1 is flip2 is flip3 is 1:
                print ("The return boolean for the flip is = %d" % flip3)
                flip1 = 0 
                flip2 = 0
                flip3 = 0
                # Giving the user time to fully flip the page
                time.sleep(2)
            if flip1 is flip2 is flip3 is -1:
                print ("The return boolean for the flip is = %d" % flip3)
                flip1 = 0 
                flip2 = 0
                flip3 = 0
                # Giving the user time to fully flip the page
                time.sleep(2)
            time.sleep(0.3)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        detect.cleanup()
