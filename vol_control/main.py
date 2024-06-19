import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hand Detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Screen dimensions for pyautogui
screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)

prev_x = 0
index_y = 0
holding = False

def adjust_brightness(frame, alpha=1.5, beta=50):
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = adjust_brightness(frame)
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    half_width = frame_width // 2
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hands.process(rgb_frame)
    hand_landmarks = output.multi_hand_landmarks

    if hand_landmarks:
        for hand in hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            landmarks = hand.landmark

            index_x = int(landmarks[8].x * frame_width)
            index_y = int(landmarks[8].y * frame_height)
            thumb_x = int(landmarks[4].x * frame_width)
            thumb_y = int(landmarks[4].y * frame_height)

            # Draw circles on the landmarks
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), -1)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255), -1)

            # Check the distance between thumb and index finger
            if abs(index_y - thumb_y) < 20:
                if not holding:
                    holding = True
                    hold_start_time = time.time()
                else:
                    hold_duration = time.time() - hold_start_time
                    if hold_duration > 0.1:  # Adjust the time as necessary
                        if index_x < half_width:
                            print("Volume Down")
                            pyautogui.press("volumedown")
                        else:
                            print("Volume Up")
                            pyautogui.press("volumeup")
                        hold_start_time = time.time()
            else:
                holding = False

    cv2.imshow('Hand Gesture Volume Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
