import cv2 as cv

cap = cv.VideoCapture("_PATH_") # 0 for web cam

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