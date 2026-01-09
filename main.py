import cv2
import mediapipe as mp
import pyautogui
from collections import deque
import time

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
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

# ---------------------------
# Webcam Setup
# ---------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# ---------------------------
# Finger detection smoothing & debounce
# ---------------------------
last_finger_counts = deque(maxlen=7)  # last 7 frames for stability
gesture_cooldown = 0.15  # seconds between same action
last_action_time = time.time()

# ---------------------------
# Finger counting function
# ---------------------------
def count_fingers(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = 0

    # Thumb
    if lm[4].x < lm[3].x:  # thumb tip left of joint
        fingers += 1

    # Other fingers
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
    # Smooth fingers using last frames
    # ---------------------------
    last_finger_counts.append(fingers)
    smooth_fingers = max(set(last_finger_counts), key=last_finger_counts.count)

    # ---------------------------
    # Debounce: prevent repeated triggers
    # ---------------------------
    current_time = time.time()
    if current_time - last_action_time < gesture_cooldown:
        smooth_fingers = 0  # ignore if cooldown not passed

    # ---------------------------
    # Custom Gesture Mapping
    # ---------------------------
    action = "NO ACTION"

    if smooth_fingers == 1:
        pyautogui.keyDown("right")
        pyautogui.keyUp("left")
        action = "MOVE RIGHT"
        last_action_time = current_time

    elif smooth_fingers == 2:
        pyautogui.keyDown("left")
        pyautogui.keyUp("right")
        action = "MOVE LEFT"
        last_action_time = current_time

    elif smooth_fingers == 3:
        pyautogui.press("space")  # jump
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")
        action = "JUMP"
        last_action_time = current_time

    elif smooth_fingers == 4:
        pyautogui.press("down")  # crunch / duck
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")
        action = "CRUNCH"
        last_action_time = current_time

    elif smooth_fingers == 5:
        pyautogui.press("ctrl")  # action / fire
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")
        action = "ACTION"
        last_action_time = current_time

    else:
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")

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
