from pdf2image import convert_from_path
import cv2
import numpy as np


class PdfFile:
    def __init__(self, filename):
        self.pages = convert_from_path(filename, 500)
        self.totalPgs = len(pages)
        return self.totalPgs

    def readPage(self, pageNum):
        if pageNum >= 0 and pageNum < self.totalPgs:
            img = cv2.cvtColor(np.array(pages[pageNum]), cv2.COLOR_RGB2BGR)
            return img
        else
            return -1


if __name__ == '__main__':
    main()
    filename = 'pdf/test1.pdf'
    pages = convert_from_path(filename, 500)

    img = pages[0]
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    height, width = img.shape[:2]
    while True:
        img = cv2.resize(img,(height//10, width//10))
        cv2.imshow('img', img)
        key = cv2.waitKey(1)
        if key == 27:
            print("stop")
            break
