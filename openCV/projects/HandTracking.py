import cv2
import mediapipe as mp
import time
import math

import pyautogui
pyautogui.FAILSAFE = False


class HandDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # hand tracking
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode, max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)
        # draw on hands
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        # finger tips id's
        self.tipIds = [4, 8, 12, 16, 20]

    def find_hands(self, frame, draw=True):
        # bgr to rgb
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # process frame
        self.results = self.hands.process(frame_rgb)
        # print(results.multi_hand_landmarks)

        # draw on hands
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw == True:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                                                )  # self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    # self.mp_drawing_styles.get_default_hand_connections_style()
        return frame

    def find_position(self, frame, hand_number=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.landmark_list = []

        if self.results.multi_hand_landmarks:
            # which hand to track
            hand = self.results.multi_hand_landmarks[hand_number]

            for id, land_mark in enumerate(hand.landmark):
                # print(id, land_mark)
                # get positions of landmarks
                height, width, channel = frame.shape
                # convert positions to pixels
                cx, cy = int(land_mark.x*width), int(land_mark.y*height)
                xList.append(cx)
                yList.append(cy)
                self.landmark_list.append([id, cx, cy])
                # print(landmark_list)
                if draw == True:
                    # index finger tip
                    if id == 8:
                        cv2.circle(frame, (cx, cy), 10,
                                   (255, 0, 255), cv2.FILLED)
            # get min and max oh hand position
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            # boundry box min and max
            bbox = xmin, ymin, xmax, ymax

            # draw boundry box around hand
            if draw:
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.landmark_list, bbox

    def fingers_up(self):
        fingers = []
        # Thumb
        # if hand landmark position is less then another landmark on same finger
        if self.landmark_list[self.tipIds[0]][1] > self.landmark_list[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
 
        # Fingers
        for id in range(1, 5):
            if self.landmark_list[self.tipIds[id]][2] < self.landmark_list[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
 
        # totalFingers = fingers.count(1)
 
        return fingers
 
    def findd_distance(self, p1, p2, frame, draw=True,r=10, t=3):
        x1, y1 = self.landmark_list[p1][1:]
        x2, y2 = self.landmark_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(frame, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
 
        return length, frame, [x1, y1, x2, y2, cx, cy]



def main():

    # capture webcam
    capture = cv2.VideoCapture(0)
    # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    #
    hand_detector = HandDetector()

    # FPS count
    previous_time = 0
    current_time = 0

    while True:
        success, frame = capture.read()
        # flip frame about the y
        frame = cv2.flip(frame, 1)
        frame = hand_detector.find_hands(frame)
        landmarks, bbox = hand_detector.find_position(frame,draw=False)
        if len(landmarks) != 0:
            print(landmarks[8])

            # move mouse
            index = landmarks[8]
            x, y = index[1], index[2]
            # moving mouse at a ratio to window size to 1080p
            # pyautogui.moveTo(x*3, int(y*2.25))
            # one to one movement
            # pyautogui.moveTo(x, int(y))

        # calculate fps
        current_time = time.time()
        fps = 1/(current_time-previous_time)
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


if __name__ == "__main__":
    main()
