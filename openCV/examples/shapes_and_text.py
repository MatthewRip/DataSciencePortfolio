import cv2 as cv
import numpy as np

img = np.zeros((512,512,3),np.uint8)

# # color img
# img[:] = 255,0,0

# draw line
# img, starting point, ending point, color, thickness
cv.line(img,(0,0),(img.shape[1],img.shape[0]),(0,255,0),3)

# draw rectangle
# img, starting point, ending point, color, thickness
cv.rectangle(img,(0,0),(250,250),(0,0,255),3)

# draw circle
# img, starting point, radius, color, thickness
cv.circle(img,(250,200),100,(255,0,255),3)

# put text on img
# img, text, where, font, fontsize, color, thicc
cv.putText(img," CUCKSAN ", (200,400),cv.FONT_ITALIC,1,(0,150,0),1)

cv.imshow('output',img)
cv.waitKey(0)