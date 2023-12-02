import cv2 as cv
import numpy as np
import argparse
import mediapipe as mp
import json

data = []

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to the input video file or 0 for webcam')
    parser.add_argument('--threshold', default=0.2, type=float)
    parser.add_argument('--width', default=368, type=int)
    parser.add_argument('--height', default=368, type=int)
    return parser.parse_args()

def detect_landmarks(frame, pose):
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    
    landmarks = results.pose_landmarks.landmark
    frame_landmark_data = {}
    for landmark, landmark_name in zip(landmarks, mp.solutions.pose.PoseLandmark):
        frame_landmark_data[landmark_name.name] = {
            "x": landmark.x,
            "y": landmark.y,
            "z": landmark.z if landmark.HasField("z") else None,
            "v": landmark.visibility,
        }
    return frame_landmark_data, results, image

def analyze_movement(frame_landmark_data, prev_landmarks, frame_counter):
    landmark_transformations = {
        "NOSE": "head",
        "RIGHT_WRIST": "rwrist",
        "RIGHT_ELBOW": "relbow",
        "RIGHT_HIP": "rleg",
        "RIGHT_KNEE": "rbody",
        "RIGHT_FOOT_INDEX": "rsupport",
        "LEFT_FOOT_INDEX": "support",
        "LEFT_WRIST": "lwrist",
        "LEFT_ELBOW": "lelbow",
        "LEFT_HIP": "lleg",
        "LEFT_KNEE": "lbody"
    }

    if prev_landmarks is not None and frame_counter % 10 == 0:
        current_time = round(frame_counter / 30.0, 1)
        found_existing_entry = False

        for entry in data:
            if entry["time"] == current_time:
                found_existing_entry = True
                for landmark_name, landmark_info in frame_landmark_data.items():
                    if landmark_name in landmark_transformations:
                        prev_info = prev_landmarks[landmark_name]
                        dx, dy, dz = landmark_info["x"] - prev_info["x"], landmark_info["y"] - prev_info["y"], landmark_info["z"] - prev_info["z"]

                        movement_direction = ""
                        if abs(dx) > 0.01:
                            movement_direction += "Left " if dx < 0 else "Right "
                        if abs(dy) > 0.05:
                            movement_direction += "Up " if dy < 0 else "Down "
                        if abs(dz) > 0.1:
                            movement_direction += "Backward " if dz < 0 else "Forward "

                        level = ""
                        if landmark_info["z"] < -0.5:
                            level = "low"
                        elif -0.5 <= landmark_info["z"] <= 0.5:
                            level = "middle"
                        else:
                            level = "high"

                        transformed_landmark_name = landmark_transformations[landmark_name]

                        if movement_direction and landmark_info["v"] > 0.5:
                            if transformed_landmark_name not in entry:
                                entry[transformed_landmark_name] = {
                                    "dur": 1.0,
                                    "dir": movement_direction.strip().lower(),
                                    "lvl": level
                                }

        if not found_existing_entry:
            movement_data = {"time": current_time}
            added_data = False
            for landmark_name, landmark_info in frame_landmark_data.items():
                if landmark_name in landmark_transformations:
                    prev_info = prev_landmarks[landmark_name]
                    dx, dy, dz = landmark_info["x"] - prev_info["x"], landmark_info["y"] - prev_info["y"], landmark_info["z"] - prev_info["z"]

                    movement_direction = ""
                    if abs(dx) > 0.01:
                        movement_direction += "Left " if dx < 0 else "Right "
                    if abs(dy) > 0.05:
                        movement_direction += "Up " if dy < 0 else "Down "
                    if abs(dz) > 0.1:
                        movement_direction += "Backward " if dz < 0 else "Forward "

                    level = ""
                    if landmark_info["z"] < -0.5:
                        level = "low"
                    elif -0.5 <= landmark_info["z"] <= 0.5:
                        level = "middle"
                    else:
                        level = "high"

                    transformed_landmark_name = landmark_transformations[landmark_name]

                    if movement_direction and landmark_info["v"] > 0.5:
                        movement_data[transformed_landmark_name] = {
                            "dur": 1.0,
                            "dir": movement_direction.strip().lower(),
                            "lvl": level
                        }
                        added_data = True

            if added_data:
                data.append(movement_data)
                print(f"Added movement data at time {current_time} seconds: {movement_data}")


def main():
    args = parse_args()
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    landmark_data_list = []

    net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

    file = args.input if args.input != "0" else 0
    cap = cv.VideoCapture(file)
    cap.set(cv.CAP_PROP_FPS, 30)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        prev_landmarks = None
        frame_counter = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame_landmark_data, results, image = detect_landmarks(frame, pose)
            landmark_data_list.append(frame_landmark_data)

            analyze_movement(frame_landmark_data, prev_landmarks, frame_counter)

            prev_landmarks = frame_landmark_data
            frame_counter += 1

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

            cv.imshow('Mediapipe Feed', image)

            if cv.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv.destroyAllWindows()

    for frame_idx, frame_landmark_data in enumerate(landmark_data_list):
        print(f"LANDMARKS - Frame {frame_idx}")
        for landmark_name, landmark_info in frame_landmark_data.items():
            print(landmark_name, "x:", landmark_info["x"], "y:", landmark_info["y"], "z:", landmark_info["z"])

    print("DATA")
    print(data)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    main()
