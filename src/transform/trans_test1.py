
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
from scipy import spatial
    
refPt = []
warp = False
    
def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        circles.append((x, y))
        
def updateTransformation(event, x, y, flags, params):
    global refPt, warp
    if event == cv2.EVENT_LBUTTONDOWN:
        print("click down")
        refPt.append((x, y))
        warp = False
    elif event == cv2.EVENT_LBUTTONUP:
        print("click up")
        circles.append((x, y))
        refPt.append((x, y))
        warp = True
    
circles = []
fr_trans = "Perspective transformation"
cv2.namedWindow(fr_trans)
cv2.setMouseCallback(fr_trans, updateTransformation)
  
debug = True  

#     _, frame = cap.read()
img = cv2.imread('img2.jpg')
height, width = img.shape[:2]
# 1280x720
proj_h = 720
proj_w = 1280
ratio = max(width/proj_w, height/proj_h);
img = cv2.resize(img, (int(width/ratio), int(height/ratio)))
img_h, img_w = img.shape[:2]
corner_img = np.array([(0, 0), (img_w, 0), (0, img_h), (img_w, img_h)])
corner_map = corner_img.copy()

while True:
    frame = img
 
    if debug:    
        cv2.circle(frame, tuple(corner_img[0]), 5, (0, 0, 255), -1)

    if warp == True:
        print("warp")
        pt = np.array(refPt[-2])
        ind = spatial.KDTree(corner_map).query(pt)[1]
        print("pos: ", pt, ". nearest! ", ind)
        corner_map[ind] = np.array(refPt[-1])
        warp = False

    matrix = cv2.getPerspectiveTransform(np.float32(corner_img), np.float32(corner_map))
    result = cv2.warpPerspective(frame, matrix, (proj_w, proj_h))

    if debug:  
        for center_position in refPt:
            cv2.circle(result, center_position, 5, (0, 255, 0), -1) 
 
 
    cv2.imshow("Frame", frame)
    cv2.imshow(fr_trans, result)
 
    key = cv2.waitKey(1)
    if key == 27:
        print("stop")
        break
 
cv2.destroyAllWindows()

