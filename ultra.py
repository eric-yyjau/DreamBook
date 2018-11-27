#Libraries
import RPi.GPIO as GPIO
import time

class Detector:
        
    #set GPIO Pins
    GPIO_TRIGGER_1 = 18   # Detecting the front flip
    GPIO_ECHO_1 = 24      # Detecting the back flip
    # GPIO_TRIGGER_2 = 18 # TODO Change to different PIN
    # GPIO_ECHO_2 = 24    # TODO Change to different PIN

    THERSHOLD = 2.0

    def setup(self, thershold = None): # TODO Check if this way of making the third argument optional has error

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER_1, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_1, GPIO.IN)
        # GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        # GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)
        
        if thershold is not None:
            self.THERSHOLD = thershold

    """
    Description:
        This function is used to calculate where the page flip occured, if/when it occured
    Return:
        Only 3 possible values
        1: Front Flip
        0: No Flip
        -1: Back Flip
    """
    def getReading(self):
        dist1 = self.__distance(self.GPIO_TRIGGER_1, self.GPIO_ECHO_1)
        print ("Measured Distance in sensor 1 = %.1f cm" % dist1)
        
        # dist2 = self.__distance(self.GPIO_TRIGGER_2, self.GPIO_ECHO_2)
        # print ("Measured Distance in sensor 2 = %.1f cm" % dist2)
        
        flip = dist1 - #dist2
        
        # First check if there was a flip
        if flip <= self.THERSHOLD:
            return 0
        
        return 1
        # Check which side is the flip. If dist1 is greater than dist2 it was front flip
        # return 1 if dist1 > dist2 else -1
 
    def __distance(self, trigger, echo):
        # set Trigger to HIGH
        GPIO.output(trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trigger, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(echo) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance

    def cleanup(self):
        GPIO.cleanup()