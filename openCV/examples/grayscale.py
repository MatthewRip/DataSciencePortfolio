import cv2 as cv
import numpy as np

img = cv.imread("images/meh.jpg", cv.IMREAD_GRAYSCALE)
img = cv.resize(img, (640, 480))

# # adding blur to img/ kernalsize has to be odd numbers
# img_blur = cv.GaussianBlur(img,(7,7),0)

cv.imshow("Output", img)
cv.waitKey(0)