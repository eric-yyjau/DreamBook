#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
import cv2
from subprocess import check_output
import numpy as np
from scipy import spatial
import time
import _thread


from transform.calibration import *
from pdf.pdf2img import PdfFile
# from rpi.page_flip import *


# In[2]:


## parameters
proj_h = 1440
proj_w = 2560

## init settings
circles = []
refPt = []
warp = False
stopReading = False


# Code structure-
# 
# Read Book:
#     Convert PDF to Images
#     Show page 1 (with transformation)
#     while (!stopReading) :
#         pageChange = Read Output Sensor
#         if pageChange == nextPage :
#             Read Page(+1)
#         else if pageChange == prevPage :
#             Read Page(-1)

# In[3]:


def get_num_pages(pdf_path):
    output = check_output(["pdfinfo", pdf_path]).decode()
    pages_line = [line for line in output.splitlines() if "Pages:" in line][0]
    num_pages = int(pages_line.split(":")[1])
    return num_pages


# In[4]:


def ConvertPdfToImages (pdfFile, imageFile) :
    
    # Path to Poppler's libraries (Download from https://blog.alivate.com.au/poppler-windows/)
    pdfToPPMPath = r"C:\Program Files (x86)\Poppler\poppler-0.68.0\bin\pdftoppm.exe"

    # Convert PDF to images
    subprocess.Popen('"%s" -png %s %s' % (pdfToPPMPath, pdfFile, imageFile))
    
    # Return number of pages in PDF
    return get_num_pages(pdfFile)


# In[ ]:


def imgResize(img):
#     img = cv2.imread(imageFile)
    height, width = img.shape[:2]
    # resize img
    ratio = max(width/proj_w, height/proj_h);
    img = cv2.resize(img, (int(width/ratio), int(height/ratio)))
    return img

def pageShow (img, mat) :
#     filename = imageFile + '-' + str(pageNumber) + '.jpg'
#     img = ReadImg(filename)
    # Open CV code for transformation
    start = time.time()
    img = cv2.warpPerspective(img, mat, (proj_w, proj_h))
    print("time warping: ", time.time()-start)

    start = time.time()
    cv2.imshow(fr_trans, img)
    print("time show: ", time.time()-start)
    start = time.time()
    key = cv2.waitKey(1)
    print("time waitkey: ", time.time()-start)

    return key
    
def initFrame(frameName):
    cv2.namedWindow(frameName)


# In[ ]:


def ReadSensorRpi(thread_name):
    import RPi.GPIO as IO
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
            
            

        if state == "hit_one" :
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


# In[ ]:


def ReadSensorOutput (threadName) :
    global page_action, detectPage
    while True:
        time.sleep(1)
        if detectPage == True:
            page_action.append(1)
        print("move forward ", page_action)
    # Return 1 for next page, -1 for prev page based on threshold
    
def ReadKeyboardInput ():
    key = []
    while True:
        key = cv2.waitKey(0)
    print("key, ", key)
    if key == 97: #'a'
        pageNum = pageNum-1
        img_next = file.readPage(pageNum)
        print ("detect a")
    elif key == 100: #'d'
        pageNum = pageNum+1
        img_next = file.readPage(pageNum)
        print ("detect d")
    


# In[ ]:


def ReadBook (pdfFile) :
    global stopReading, fr_trans, page_action, detectPage
    detectPage = True
    page_action = []
    file = PdfFile()
    totalPages = file.readFile(pdfFile)
    print("total: ", totalPages)
    if totalPages < 1:
        return -1
    pageNumber = 0
    img = file.readPage(pageNumber)
    img = imgResize(img)
    # calibration
    mat = np.identity(3)
    mat = calibration(img)
    print("img shape: ", img.shape)
    pageShow(img, mat)
    pageChange = 0
    while (stopReading == False) : # Replace with a listener to signal end of reading
        detectPage = True
        pageChange = 0
        if len(page_action)>0:
            pageChange = page_action[-1]
            print("get page change ", pageChange)
            del page_action[-1]
        # time.sleep(0.5)
#         pageChange = ReadSensorOutput()
#         pageChange = ReadKeyboardInput()
        key = pageShow(img, mat)
        if key == 27:
            print("stop")
            break
        elif key == 97: #'a'
            pageChange = 1
            print ("detect a")
        elif key == 100: #'d'
            pageChange = -1
            print ("detect d")
#         page changing    
        if pageChange==1 and pageNumber<totalPages-1 : 
            pageNumber = pageNumber + 1
            print(pageNumber)
            start = time.time()
            img = file.readPage(pageNumber)
            print("time read: ", time.time()-start)
            start = time.time()
            img = imgResize(img)
            print("time resize: ", time.time()-start)
        elif pageChange==-1 and pageNumber>0 :
            pageNumber = pageNumber - 1
            img = imgResize(file.readPage(pageNumber))
        time.sleep(0.01)
    detectPage = False
#     cv2.destroyWindow(fr_trans)


# In[ ]:


def print_time( threadName):
       delay = 1
       count = 0
       while count < 5:
          time.sleep(delay)
          count += 1
          print ("%s: %s" % ( threadName, time.ctime(time.time()) ))


# In[ ]:


def readNameFromFolder(folderName):
    import os
    pdfFiles = []
    for file in os.listdir(folderName):
        if file.endswith(".pdf"):
            pdfFiles.append(os.path.join(folderName, file))
            print(os.path.join(folderName, file))
    return pdfFiles


# In[1]:


if __name__ == "__main__":
#     pdfFile = "pdf/test1.pdf"
    detectPage = True
    rpi_sensor = True
    page_action = []
    folderName = "pdf/"
    pdfFiles = readNameFromFolder(folderName)
    imgBlack = np.zeros((proj_h, proj_w))
    if pdfFiles != []:
        # page detection
        try:
            if rpi_sensor == True:
                print("R pi sensor")
                ReadSensorRpi
                _thread.start_new_thread( ReadSensorRpi, ("Thread-1",))
#                 _thread.start_new_thread( ReadSensor, ("Thread-1",detectPage,page_action))
            else:
                print("Testing")
                _thread.start_new_thread( ReadSensorOutput, ("Thread-2",))
        except:
            print ("Error: unable to start thread")
        fr_trans = "Perspective transformation"
        initFrame(fr_trans)
        print("Please select a file!")
        fileIdx = 0
        def IdxChange(idx, action, numMax, minMax):
            result = idx + action
            if result >= minMax and result <= numMax:
                idx = result
            else:
                result = idx
            return result
        while True:
            cv2.imshow(fr_trans, imgBlack)
            key = cv2.waitKey(1)
            if key == 27:
                print("stop")
                break
            elif key == 13:
                print("Enter")
                print("read file: ", pdfFiles[fileIdx])
                ReadBook (pdfFiles[fileIdx])
            elif key == 97: #'a'
                fileIdx = IdxChange(fileIdx, -1, 0, len(pdfFiles)-1)
                print ("detect a")
            elif key == 100: #'d'
                fileIdx = IdxChange(fileIdx, +1, 0, len(pdfFiles)-1)
                print ("detect d")


    
    cv2.destroyAllWindows()
    
    


# In[ ]:





# In[ ]:


detectPage = False


# In[ ]:


detectPage
ReadSensor("",1,2)


# In[ ]:


_thread.start_new_thread( ReadSensorRpi, ("Thread-1",))


# In[ ]:




