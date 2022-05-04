import cv2
import mediapipe as mp
import time

# capture webcam
capture = cv2.VideoCapture(0)

# hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
# draw on hands
mp_draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# FPS count
previous_time = 0
current_time = 0


while True:
    success, frame = capture.read()
    # flip frame about the y
    frame = cv2.flip(frame, 1)
    # bgr to rgb
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # process frame
    results = hands.process(frame_rgb)
    # print(results.multi_hand_landmarks)

    # draw on hands
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, land_mark in enumerate(hand_landmarks.landmark):
                # print(id, land_mark)
                # get positions of landmarks
                height, width, channel = frame.shape
                # convert positions to pixels
                cx, cy = int(land_mark.x*width), int(land_mark.y*height)
                # index finger tip
                if id == 8:
                    cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                   mp_drawing_styles.get_default_hand_landmarks_style(),
                                   mp_drawing_styles.get_default_hand_connections_style()
                                   )

    # calculate fps
    current_time = time.time()
    fps = 1/(current_time-previous_time)
    previous_time = current_time
    # display fps
    cv2.putText(frame, str(int(fps)), (10, 30),
                cv2.FONT_ITALIC, 1, (0, 255, 0), 2)

    # display capture
    cv2.imshow("Output", frame)
    # close
    if cv2.waitKey(1) == ord('q'):
        capture.release()
        cv2.destroyAllWindows()
        break