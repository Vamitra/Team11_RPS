import cv2
import numpy as np
import random
import time

def get_hand_gesture(contour, hull, defects):
    if defects is None:
        return "Rock", 0
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

        # Improved detection with angle and depth threshold
        if angle <= 1.5 and d > 10000:
            finger_count += 1

    if finger_count == 0:
        return "Rock", finger_count
    elif 1 <= finger_count <= 2:
        return "Scissors", finger_count
    elif finger_count >= 3:
        return "Paper", finger_count
    return "Invalid", finger_count

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

def countdown_animation(frame_width, frame_height):
    for count in ["3", "2", "1", "GO!"]:
        frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        color = (0, 0, 255) if count != "GO!" else (0, 255, 0)
        font_scale = 4 if count != "GO!" else 3
        text_size = cv2.getTextSize(count, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 5)[0]
        text_x = (frame_width - text_size[0]) // 2
        text_y = (frame_height + text_size[1]) // 2
        cv2.putText(frame, count, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 5)
        cv2.imshow("Rock Paper Scissors", frame)
        cv2.waitKey(1000)

# Your setup values
cap = cv2.VideoCapture(0)
frame_width = 1080
frame_height = 720
roi_size = 400
center_x = frame_width // 2
center_y = frame_height // 2
x1 = center_x - roi_size // 2
y1 = center_y - roi_size // 2
x2 = x1 + roi_size
y2 = y1 + roi_size

# Game state
last_result = ""
ai_move = ""
user_move = ""
finger_count = 0
last_time = 0
player_score = 0
ai_score = 0
rounds_played = 0
started = False
show_instructions = False
game_started = False

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (frame_width, frame_height))
        key = cv2.waitKey(1)

        if player_score == 3 or ai_score == 3:
            winner = "You Win!" if player_score == 3 else "AI Wins!"
            frame[:] = (0, 0, 0)
            cv2.putText(frame, "GAME OVER", (350, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)
            cv2.putText(frame, winner, (420, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
            cv2.putText(frame, "Press 'r' to restart or 'q' to quit", (240, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            cv2.imshow("Rock Paper Scissors", frame)

            if key == ord('r'):
                player_score = ai_score = rounds_played = 0
                user_move = ai_move = last_result = ""
                started = show_instructions = game_started = False
            elif key == ord('q'):
                break
            continue

        if game_started:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        roi = frame[y1:y2, x1:x2]

        if not started:
            title = "Rock Paper Scissors"
            subtitle = "Press 's' to Start"
            title_scale = 1.8
            subtitle_scale = 1.2

            title_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, title_scale, 3)[0]
            subtitle_size = cv2.getTextSize(subtitle, cv2.FONT_HERSHEY_SIMPLEX, subtitle_scale, 2)[0]

            title_x = (frame_width - title_size[0]) // 2
            subtitle_x = (frame_width - subtitle_size[0]) // 2

            center_y = frame_height // 2
            title_y = center_y - 40
            subtitle_y = center_y + 40

            cv2.putText(frame, title, (title_x, title_y), cv2.FONT_HERSHEY_SIMPLEX, title_scale, (0, 0, 0), 3)
            cv2.putText(frame, subtitle, (subtitle_x, subtitle_y), cv2.FONT_HERSHEY_SIMPLEX, subtitle_scale, (0, 0, 255), 2)
            cv2.imshow("Rock Paper Scissors", frame)

            if key == ord('s'):
                started = True
                show_instructions = True
            elif key == ord('q'):
                break
            continue

        if show_instructions:
            cv2.putText(frame, "Instructions", (430, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3)
            cv2.putText(frame, "ROCK", (180, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 3)
            cv2.putText(frame, "PAPER", (470, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 3)
            cv2.putText(frame, "SCISSORS", (730, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 3)
            cv2.putText(frame, "Make a fist", (170, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (50, 50, 50), 2)
            cv2.putText(frame, "Open your palm", (450, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (50, 50, 50), 2)
            cv2.putText(frame, "Hold up 2 fingers", (710, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (50, 50, 50), 2)
            cv2.putText(frame, "- Keep hand inside the blue box", (100, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(frame, "- You get 5 seconds per move", (100, 370), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(frame, "- Press 'n' to begin the game", (100, 430), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.imshow("Rock Paper Scissors", frame)

            if key == ord('n'):
                show_instructions = False
                countdown_animation(frame_width, frame_height)
                game_started = True
            elif key == ord('q'):
                break
            continue

        cv2.putText(frame, "Put hand in box. Press 'q' to quit.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80, 80, 80), 2)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (35, 35), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(contour) > 5000:
                hull = cv2.convexHull(contour)
                defects = cv2.convexityDefects(contour, cv2.convexHull(contour, returnPoints=False))
                user_move, finger_count = get_hand_gesture(contour, hull, defects)
                if cv2.getTickCount() - last_time > cv2.getTickFrequency() * 5:
                    ai_move = get_ai_move()
                    last_result = get_winner(user_move, ai_move)
                    if last_result == "You Win!":
                        player_score += 1
                    elif last_result == "AI Wins!":
                        ai_score += 1
                    last_time = cv2.getTickCount()
                    rounds_played += 1
            else:
                user_move = "Invalid"
                finger_count = 0
        else:
            user_move = "Invalid"
            finger_count = 0

        base_y = 100
        line_height = 40
        font_scale = 0.8
        cv2.putText(frame, f"You: {user_move}", (30, base_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)
        cv2.putText(frame, f"AI: {ai_move}", (30, base_y + line_height), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)
        cv2.putText(frame, f"Result: {last_result}", (30, base_y + 2 * line_height), cv2.FONT_HERSHEY_SIMPLEX, font_scale + 0.1, (0, 0, 255), 2)
        cv2.putText(frame, f"Fingers: {finger_count}", (30, base_y + 3 * line_height), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (128, 0, 128), 2)
        cv2.putText(frame, f"Score - You: {player_score} | AI: {ai_score}", (30, base_y + 4 * line_height), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (50, 100, 255), 2)

        cv2.imshow("Rock Paper Scissors", frame)
        cv2.namedWindow("Threshold", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Threshold", 400, 400)
        cv2.imshow("Threshold", thresh)

        if key == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
