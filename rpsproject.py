import cv2
import numpy as np
import random

def get_hand_gesture(contour, hull, defects):
    if defects is None:
        return "Rock"

    finger_count = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        a = np.linalg.norm(np.array(end) - np.array(start))
        b = np.linalg.norm(np.array(far) - np.array(start))
        c = np.linalg.norm(np.array(end) - np.array(far))
        angle = np.arccos((b**2 + c**2 - a**2)/(2*b*c))

        if angle <= np.pi / 2:
            finger_count += 1

    if finger_count == 0:
        return "Rock"
    elif 1 <= finger_count <= 2:
        return "Scissors"
    elif finger_count >= 3:
        return "Paper"
    return "Unknown"

def get_ai_move():
    return random.choice(["Rock", "Paper", "Scissors"])

def get_winner(user, ai):
    if user == ai:
        return "Draw"
    elif (user == "Rock" and ai == "Scissors") or \
         (user == "Scissors" and ai == "Paper") or \
         (user == "Paper" and ai == "Rock"):
        return "You Win!"
    else:
        return "AI Wins!"

cap = cv2.VideoCapture(0)
last_result = ""
ai_move = ""
user_move = ""
last_time = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        roi = frame[100:400, 100:400]
        cv2.rectangle(frame, (100, 100), (400, 400), (255, 0, 0), 2)

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (35, 35), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            contour = max(contours, key=cv2.contourArea)

            if cv2.contourArea(contour) > 5000:
                hull = cv2.convexHull(contour)
                defects = cv2.convexityDefects(contour, cv2.convexHull(contour, returnPoints=False))

                user_move = get_hand_gesture(contour, hull, defects)

                if cv2.getTickCount() - last_time > cv2.getTickFrequency() * 2:
                    ai_move = get_ai_move()
                    last_result = get_winner(user_move, ai_move)
                    last_time = cv2.getTickCount()

        # Display
        cv2.putText(frame, f"You: {user_move}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(frame, f"AI: {ai_move}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,255,100), 2)
        cv2.putText(frame, f"Result: {last_result}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        cv2.imshow("Rock Paper Scissors (No MediaPipe)", frame)
        cv2.imshow("Threshold", thresh)

        # Exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting the game...")
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
