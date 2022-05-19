from enum import auto
import cv2
import numpy as np
import time
import HandTracking as ht
import autopy
import pyautogui

# for fps
previous_time = 0
# cam resolution
cam_width, cam_hieght = 640, 480
# screen resolution
screen_width, screen_height = autopy.screen.size()
# frame reduction
boundary_reduction_x = 250
boundary_reduction_y = 175

# smoothening factor
smoothen_mouse_factor = 20
# previous location of x, y
pre_x, pre_y = 0, 0
# current location of x, y
curr_x, curr_y = 0, 0

# capture webcam
capture = cv2.VideoCapture(0)
# set cam resolution
capture.set(3, cam_width)
capture.set(4, cam_hieght)
# hand detector
hand_detector = ht.HandDetector(detectionCon=0.7,trackCon=0.7)


while True:
    # read frame from capture
    success, frame = capture.read()
    # flip capture
    frame = cv2.flip(frame, 1)
    # find hand landmarks and boundary box
    frame = hand_detector.find_hands(frame, draw=False)
    landmark_list, boundary_box = hand_detector.find_position(
        frame, draw=False)

    # get fingers
    if len(landmark_list) != 0:
        # index finger
        x1, y1 = landmark_list[8][1:]
        # middle finger
        x2, y2 = landmark_list[12][1:]
        # check which fingers are up
        fingers = hand_detector.fingers_up()
        # print(fingers)
        # screen boundary box
        cv2.rectangle(frame, (boundary_reduction_x, boundary_reduction_y), (
            cam_width-boundary_reduction_x, cam_hieght-boundary_reduction_y), (255, 0, 255), 2)
        # 4. only index finger : moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            # convert coordinates / change ratio
            x3 = np.interp(x1, (boundary_reduction_x, cam_width -
                                boundary_reduction_x), (0, screen_width))
            y3 = np.interp(y1, (boundary_reduction_y, cam_hieght -
                                boundary_reduction_y), (0, screen_height))
            # smooth mouse movement
            curr_x = pre_x+(x3-pre_x)/smoothen_mouse_factor
            curr_y = pre_y+(y3-pre_y)/smoothen_mouse_factor
            pre_x, pre_y = curr_x, curr_y
            # move mouse
            autopy.mouse.move(curr_x, curr_y)
            # when index finger is up draw
            cv2.circle(frame, (x1, y1), 5, (255, 0, 0), cv2.FILLED)

        # index and middle fingers are up
        if fingers[1] == 1 and fingers[2] == 1:
            # length, frame, line_info = hand_detector.findd_distance(
            #     8, 12, frame)
            # # print(length)
            # # when both index and middle fingers are up then click
            # if length < 7:
            #     cv2.circle(
            #         frame, (line_info[4], line_info[5]), 5, (0, 255, 0), cv2.FILLED)
            #     autopy.mouse.click()

            # convert coordinates / change ratio
            x3 = np.interp(x1, (boundary_reduction_x, cam_width -
                                boundary_reduction_x), (0, screen_width))
            y3 = np.interp(y1, (boundary_reduction_y, cam_hieght -
                                boundary_reduction_y), (0, screen_height))
            # smooth mouse movement
            curr_x = pre_x+(x3-pre_x)/smoothen_mouse_factor
            curr_y = pre_y+(y3-pre_y)/smoothen_mouse_factor
            pre_x, pre_y = curr_x, curr_y
            
            length, frame, line_info = hand_detector.findd_distance(
                8, 12, frame)
            # print(length)
            # when both index and middle fingers are up then click
            if length > 30:
                pyautogui.click()
            elif length < 40:
                cv2.circle(
                    frame, (line_info[4], line_info[5]), 5, (0, 255, 0), cv2.FILLED)
                pyautogui.mouseDown(x=curr_x,y=curr_y,duration=1.0)
                
            
                

    # frame rate
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    # display fps
    cv2.putText(frame, str(int(fps)), (10, 30),
                cv2.FONT_ITALIC, 1, (0, 255, 0), 2)

    # display capture
    cv2.imshow("Ouqtput", frame)
    # close
    if cv2.waitKey(1) == ord('q'):
        capture.release()
        cv2.destroyAllWindows()
        break
