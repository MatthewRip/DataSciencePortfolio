import cv2 as cv

img = "images/meh.jpg"

# read img
img = cv.imread(img)
# show
cv.imshow("Output",img)
# terminate
cv.waitKey(0)