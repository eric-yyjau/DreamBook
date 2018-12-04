from pdf2image import convert_from_path
import cv2
import numpy as np


class PdfFile:
    def __init__(self):
        pass

    def readFile(self, filename):
        self.pages = convert_from_path(filename, 500)
        self.totalPgs = len(self.pages)
        return self.totalPgs

    def readPage(self, pageNum):
        if pageNum >= 0 and pageNum < self.totalPgs:
            img = cv2.cvtColor(np.array(self.pages[pageNum]), cv2.COLOR_RGB2BGR)
            return img
        else:
            return -1


if __name__ == '__main__':
    filename = 'pdf/test1.pdf'
    file = PdfFile()
    totalPgs = file.readFile(filename)
    print("total pages = ", totalPgs)

    img = file.readPage(0)
    height, width = img.shape[:2]
    while True:
        img = cv2.resize(img,(height//10, width//10))
        cv2.imshow('img', img)
        key = cv2.waitKey(1)
        if key == 27:
            print("stop")
            break
