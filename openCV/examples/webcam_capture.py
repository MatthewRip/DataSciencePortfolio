import cv2 as cv

# 0 == default webcam
cap = cv.VideoCapture(0)
# set parameters for capture
# 3 == width
cap.set(3, 640)
# 4 == height
cap.set(4,480)
# 10 == brightness
cap.set(10,100)

# have to loop through vid because its just a series of img's
while True:
    # if successful , image
    success, img = cap.read()
    cv.imshow("Video",img)
    # press 'q' with output window focused to exit.
    # waits 1ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break