from pdf2image import convert_from_path
import cv2
import numpy as np
import time


class PdfFile:
    def __init__(self):
        self.pages = []
        self.totalPgs = 0
        pass

    def readFile(self, filename):
        self.pages = convert_from_path(filename)
        self.totalPgs = len(self.pages)
        self.convertPgs()
        return self.totalPgs

    def readPage(self, pageNum):
        if pageNum >= 0 and pageNum < self.totalPgs:
            # img = cv2.cvtColor(np.array(self.pages[pageNum]), cv2.COLOR_RGB2BGR)
            img = self.pages[pageNum]
            return img
        else:
            print("out of range")
            return []
    def convertPgs (self):
        for i in range(self.totalPgs):
            self.pages[i] = cv2.cvtColor(np.array(self.pages[i]), cv2.COLOR_RGB2BGR)
    def getTotalPgs(self):
        return self.totalPgs
    def getAllPgs(self):
        return self.pages



if __name__ == '__main__':
    filename = 'test1.pdf'
    file = PdfFile()
    totalPgs = file.readFile(filename)
    print("total pages = ", totalPgs)

    pageNum = 0
    img = file.readPage(pageNum)
    img_next = []
    height, width = img.shape[:2]
    while True:
        img = cv2.resize(img,(height//10, width//10))
        cv2.imshow('img', img)
        key = cv2.waitKey(1)
        if key == 97: #'a'
            pageNum = pageNum-1
            img_next = file.readPage(pageNum)
            print ("detect a")
        elif key == 100: #'d'
            pageNum = pageNum+1
            img_next = file.readPage(pageNum)
            print ("detect d")
        if img_next != []:
            img = img_next

        if key == 27:
            print("stop")
            break
        time.sleep(0.1)
        # else if key == 
