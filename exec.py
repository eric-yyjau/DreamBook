import time
from ultra import Detector

if __name__ == '__main__':
    try:
        detect = Detector()
        detect.setup()
        while True:
            flipOccured = detect.getReading()
            print ("The return boolean for the flip is = %d" % flipOccured)
            time.sleep(0.3)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        detect.cleanup()
