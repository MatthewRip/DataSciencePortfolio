import cv2 as cv
import numpy as np

img = cv.imread("images/meh.jpg")
print(img.shape)
# height, width, channel

img_resize = cv.resize(img,(640,480))

# img is just an array of pixels 
img_cropped = img[0:200,200:500]

cv.imshow("Img",img_resize)
cv.imshow("cropped",img_cropped)
cv.waitKey(0)