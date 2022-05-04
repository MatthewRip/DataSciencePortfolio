"""
using warp prespective to get an birds eye view

"""


import cv2
import numpy as np

img = cv2.imread("images/cards.jpg")

# size of card
width,height = 250,350

# define 4 corner points of card
# ([[Top left],[Top right],[Bottom right],[Bottom left]]) points in img
pts1 = np.float32([[656, 251],[1087, 318], [482, 594], [970, 682]])
# defining where the points are on the img
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
# matrix 
matrix = cv2.getPerspectiveTransform(pts1,pts2)

img_output = cv2.warpPerspective(img,matrix,(width,height))


cv2.imshow("Output", img)
cv2.imshow("warped Output", img_output)

cv2.waitKey(0)