import cv2
import mediapipe as mp
import pyautogui
from collections import deque

# ---------------------------
# PyAutoGUI setup
# ---------------------------
pyautogui.FAILSAFE = False

# ---------------------------
# MediaPipe Hands Setup
# ---------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ---------------------------
# Webcam Setup
# ---------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# ---------------------------
# Finger detection smoothing
# ---------------------------
last_finger_counts = deque(maxlen=5)  # last 5 frames

# ---------------------------
# Finger counting function
# ---------------------------
def count_fingers(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = 0

    # Thumb (x coordinate)
    if lm[4].x < lm[3].x:
        fingers += 1

    # Other fingers (y coordinate)
    for tip in [8, 12, 16, 20]:
        if lm[tip].y < lm[tip - 2].y:
            fingers += 1

    return fingers

# ---------------------------
# Main loop
# ---------------------------
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    fingers = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = count_fingers(hand_landmarks)

    # ---------------------------
    # Smooth fingers using last 5 frames
    # ---------------------------
    last_finger_counts.append(fingers)
    smooth_fingers = max(set(last_finger_counts), key=last_finger_counts.count)

    # ---------------------------
    # Gesture mapping to keys
    # ---------------------------
    if smooth_fingers == 1:
        pyautogui.keyDown("left")
        pyautogui.keyUp("right")
        action = "MOVE LEFT"
    elif smooth_fingers == 2:
        pyautogui.keyDown("right")
        pyautogui.keyUp("left")
        action = "MOVE RIGHT"
    elif smooth_fingers == 3:
        pyautogui.press("space")  # jump
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")
        action = "JUMP"
    elif smooth_fingers == 5:
        pyautogui.press("ctrl")  # action / fire
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")
        action = "ACTION"
    else:
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")
        action = "NO ACTION"

    # ---------------------------
    # Display action on screen
    # ---------------------------
    cv2.putText(img, f"Action: {action}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Game Controller", img)

    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
