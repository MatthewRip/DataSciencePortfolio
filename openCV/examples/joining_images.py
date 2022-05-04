""" joining multiple imgs into one window """

import cv2
import numpy as np


img = cv2.imread("images/meh.jpg")
img = cv2.resize(img, (640, 480))

horizontal_stack = np.hstack((img, img))
vertical_stack = np.vstack((img,img))

cv2.imshow("H Output", horizontal_stack)
cv2.imshow("V Output", vertical_stack)

cv2.waitKey(0)
