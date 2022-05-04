import cv2
import numpy as np


def stackImage(scale, images):
    width = images[0][0].shape[1]
    height = images[0][0].shape[0]
    ver = None
    for img in images:
        hor = None
        for i in img:
            if i.shape[:2] == images[0][0].shape[:2]:
                i = cv2.resize(i, (0, 0), None, scale, scale)
            else:
                i = cv2.resize(i, (width, height), None, scale, scale)

            if len(i.shape) == 2:
                i = cv2.cvtColor(i, cv2.COLOR_GRAY2BGR)

            if hor is not None:
                hor = np.hstack((hor, i))
            else:
                hor = i
        if ver is not None:
            ver = np.vstack((ver, hor))
        else:
            ver = hor
    return ver


def get_contours(img):
    # outer corners
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        # cv2.drawContours(img_copy, cnt, -1, (255, 0, 0), 3)
        """if area > 500px"""
        if area > 500:
            cv2.drawContours(img_copy, cnt, -1, (255, 0, 0), 3)
            # lenght
            parameter = cv2.arcLength(cnt, True)
            # corner points
            approximate = cv2.approxPolyDP(cnt, 0.02 * parameter, True)
            object_corners = len(approximate)
            # boundary box
            x, y, w, h = cv2.boundingRect(approximate)
            # draw
            cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,0,255),5)


img = cv2.imread("images/shapes.jpg")
# copy
img_copy = img.copy()
# covert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur
img_blur = cv2.GaussianBlur(img_gray, (7, 7), 1)
# edge detection
img_canny = cv2.Canny(img_blur, 50, 50)

# draw contours
get_contours(img_canny)


img = stackImage(0.7, [[img, img, img_gray],
                       [img_blur, img_canny, img_copy]])


cv2.imshow("Output", img)
cv2.waitKey(0)