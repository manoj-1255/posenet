import cv2
import mediapipe as mp
import streamlit as st
import numpy as np
from plans import get_fitness_plan

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle if angle <= 180 else 360 - angle

def fitness_tracker(bmi, age, gender, day):
    _, exercise_plan = get_fitness_plan(bmi, age, gender)
    counters = {exercise: 0 for exercise in exercise_plan.keys()}
    stages = {exercise: None for exercise in exercise_plan.keys()}

    # Ensure current exercise is initialized
    if st.session_state.current_exercise is None:
        st.session_state.current_exercise = list(exercise_plan.keys())[0]

    current_exercise = st.session_state.current_exercise

    st.title("Fitness Tracker")
    cap = cv2.VideoCapture(0)
    
    # Video recording setup
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'day_{day}_session.avi', fourcc, 20.0, (640, 480))  # Output video file

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Unable to access camera.")
                break

            frame = cv2.resize(frame, (640, 480))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Coordinates for relevant joints
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Angle calculations for exercises
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Exercise-specific logic
                if current_exercise == "Left Curl":
                    if left_angle > 160:
                        stages[current_exercise] = "down"
                    if left_angle < 30 and stages[current_exercise] == "down":
                        stages[current_exercise] = "up"
                        counters[current_exercise] += 1

                elif current_exercise == "Right Curl":
                    if right_angle > 160:
                        stages[current_exercise] = "down"
                    if right_angle < 30 and stages[current_exercise] == "down":
                        stages[current_exercise] = "up"
                        counters[current_exercise] += 1

                elif current_exercise == "Push-ups":
                    if left_angle > 140 and right_angle > 140:
                        stages[current_exercise] = "down"
                    if left_angle < 90 and right_angle < 90 and stages[current_exercise] == "down":
                        stages[current_exercise] = "up"
                        counters[current_exercise] += 1

                elif current_exercise == "Squats":
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    situp_angle = calculate_angle(hip, knee, ankle)
                    if situp_angle > 160:
                        stages[current_exercise] = "down"
                    if situp_angle < 70 and stages[current_exercise] == "down":
                        stages[current_exercise] = "up"
                        counters[current_exercise] += 1

                # Display the counter for the current exercise
                cv2.putText(
                    frame,
                    f'{current_exercise} Count: {counters[current_exercise]}',
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA
                )

                # Record the video frame
                out.write(frame)

                # Check if the goal is achieved
                if counters[current_exercise] >= exercise_plan[current_exercise]:
                    st.success(f"Completed {current_exercise}!")
                    if current_exercise == list(exercise_plan.keys())[-1]:  # Last exercise
                        cap.release()
                        out.release()  # Save the video file
                        cv2.destroyAllWindows()
                        stframe.text("Congratulations! You have completed today's fitness plan.")
                        if st.button("Next"):
                            st.session_state.exercise_complete = False  # Reset state
                            st.session_state.current_exercise = None  # Reset exercise tracking
                            fitness_tracker(bmi, age)  # Restart the tracker
                        return

                    else:
                        # Move to next exercise
                        current_exercise = list(exercise_plan.keys())[list(exercise_plan.keys()).index(current_exercise) + 1]

            # Display frame
            stframe.image(frame, channels="BGR")

            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    cap.release()
    out.release()  # Save the video file
    cv2.destroyAllWindows()
