import cv2 as cv
import numpy as np

img = cv.imread("images/meh.jpg", cv.IMREAD_GRAYSCALE)
img = cv.resize(img, (640, 480))

# define kernal for cv.dilate
kernal = np.ones((5, 5), np.uint8)

# # adding blur to img/ kernalsize has to be odd numbers
# img_blur = cv.GaussianBlur(img,(7,7),0)

# edge detection
img_canny = cv.Canny(img, 100, 100)
img_dialation = cv.dilate(img_canny,kernal,iterations=1)
img_eroded = cv.erode(img_dialation,kernal,iterations=1)

cv.imshow("canny", img_canny)
cv.imshow("dilate", img_dialation)
cv.imshow("erotion", img_eroded)
cv.waitKey(0)
