import cv2
import numpy as np


def empty(something):
    pass


path = 'images/cards.jpg'


cv2.namedWindow("Track Bars")
cv2.resizeWindow("Track Bars", 640, 240)
cv2.createTrackbar("Hue Min", "Track Bars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "Track Bars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "Track Bars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "Track Bars", 255, 255, empty)
cv2.createTrackbar("Val Min", "Track Bars", 0, 255, empty)
cv2.createTrackbar("Val Max", "Track Bars", 255, 255, empty)

while True:
    img = cv2.imread(path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_min = cv2.getTrackbarPos("Hue Min", "Track Bars")
    hue_max = cv2.getTrackbarPos("Hue Max", "Track Bars")
    sat_min = cv2.getTrackbarPos("Sat Min", "Track Bars")
    sat_max = cv2.getTrackbarPos("Sat Max", "Track Bars")
    val_min = cv2.getTrackbarPos("Val Min", "Track Bars")
    val_max = cv2.getTrackbarPos("Val Max", "Track Bars")
    print(hue_min, hue_max, sat_min, sat_max, val_min, val_max)

    lower_limit = np.array([hue_min, sat_min, val_min])
    upper_limit = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(img_hsv, lower_limit, upper_limit)
    # create new img from orginal img where mask img pixels are white
    img_result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("Original", img)
    cv2.imshow("HSV", img_hsv)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", img_result)
    cv2.waitKey(1)
n