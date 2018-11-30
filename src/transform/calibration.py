
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
from scipy import spatial
    
debug = True  

## parameters
proj_h = 720
proj_w = 1280

## init settings
circles = []
refPt = []
warp = False

        
def updateTransformation(event, x, y, flags, params):
    global refPt, warp
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        warp = False
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        warp = True


def calibration(frame_orig):
    global warp
    fr_trans = "Perspective transformation"
    cv2.namedWindow(fr_trans)
    cv2.setMouseCallback(fr_trans, updateTransformation)
    img_h, img_w = frame_orig.shape[:2]
    corner_img = np.array([(0, 0), (img_w, 0), (0, img_h), (img_w, img_h)])
    corner_map = corner_img.copy()
    matrix = []
    while True:
        if debug:    
            cv2.circle(frame_orig, tuple(corner_img[0]), 5, (0, 0, 255), -1)

        if warp == True:
            print("warp")
            pt = np.array(refPt[-2])
            ind = spatial.KDTree(corner_map).query(pt)[1]
            print("pos: ", pt, ". nearest! ", ind)
            corner_map[ind] = np.array(refPt[-1])
            warp = False

        matrix = cv2.getPerspectiveTransform(np.float32(corner_img), np.float32(corner_map))
        frame_proj = cv2.warpPerspective(frame_orig, matrix, (proj_w, proj_h))

        if debug:  
            for pt in refPt:
                cv2.circle(frame_proj, pt, 5, (0, 255, 0), -1) 
     
     
        cv2.imshow("Frame", frame_orig)
        cv2.imshow(fr_trans, frame_proj)
     
        key = cv2.waitKey(1)
        if key == 27:
            print("stop")
            break
 
    cv2.destroyAllWindows()
    return matrix

if __name__ == "__main__":
    filename = 'img2.jpg'
    img = cv2.imread(filename)
    height, width = img.shape[:2]

    # resize img
    ratio = max(width/proj_w, height/proj_h);
    img = cv2.resize(img, (int(width/ratio), int(height/ratio)))

    # set frames
    fr_trans = "Perspective transformation"
    cv2.namedWindow(fr_trans)
    cv2.setMouseCallback(fr_trans, updateTransformation)

    mat = calibration(img)

