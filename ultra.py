#Libraries
import RPi.GPIO as GPIO
import time

class Detector:
        
    #set GPIO Pins
    GPIO_TRIGGER_1 = 18   # Detecting the front flip
    GPIO_ECHO_1 = 24      # Detecting the back flip
    GPIO_TRIGGER_2 = 22   
    GPIO_ECHO_2 = 17   

    THERSHOLD = 3

    runningSum1 = 0
    runningSum2 = 0
    counter = 0

    def setup(self, thershold = None): 

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER_1, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_1, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)
        
        if thershold is not None:
            self.THERSHOLD = thershold

    """
    Description:
        This function is used to calculate where the page flip occured, if/when it occured
    Return:
        Only 3 possible values; 1, 0, -1
    """
    def getReading(self):
        dist1 = 0
        dist2 = 0

        while dist1 < 1 or dist2 < 1:
            dist1 = self.getDistance(self.GPIO_TRIGGER_1, self.GPIO_ECHO_1) 
            print ("Measured Distance in sensor 1 (pin 24 & 18) = %.1f cm" % dist1)
            
            dist2 = self.getDistance(self.GPIO_TRIGGER_2, self.GPIO_ECHO_2)
            print ("Measured Distance in sensor 2 (pin 22 & 17) = %.1f cm" % dist2)

        self.runningSum1 += dist1
        self.runningSum2 += dist2
        self.counter = self.counter + 1

        flip = abs(dist1 - dist2)

        if flip <= self.THERSHOLD:
            return 0
        
        return 1 if dist1 > dist2 else -1

    # Get average of four readin
    def getDistance(self, trigger, echo):
        dist = 0

        dist += self.__distance(trigger, echo)
        dist += self.__distance(trigger, echo)
        dist += self.__distance(trigger, echo)
        dist += self.__distance(trigger, echo)

        dist = dist / 4;


        return dist

 
    def __distance(self, trigger, echo):
        # set Trigger to HIGH
        GPIO.output(trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trigger, False)
    
        StartTime = time.time()
        tempStartTime = StartTime
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(echo) == 0:
            StartTime = time.time()
            if StartTime > tempStartTime + 1:
                print ("Time out when getting the start time")
                return 0
    
        # save time of arrival
        while GPIO.input(echo) == 1:
            StopTime = time.time()
            if StopTime > StartTime + 1:
                print ("Time out when getting the stop time")
                return 0
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance

    def cleanup(self):
        avg1 = float(self.runningSum1) / self.counter
        avg2 = float(self.runningSum2) / self.counter
        print ("Average of the first sensor: %.1f\nAverage of second sensor: %.1f" % (avg1, avg2))
        GPIO.cleanup()
