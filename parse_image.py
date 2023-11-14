import cv2 as cv
import numpy as np
import argparse
import mediapipe as mp

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
        }
    return frame_landmark_data, results, image

def analyze_movement(frame_landmark_data, prev_landmarks, frame_counter):
    if prev_landmarks is not None and frame_counter % 10 == 0:
        for landmark_name, landmark_info in frame_landmark_data.items():
            prev_info = prev_landmarks[landmark_name]
            dx, dy, dz = landmark_info["x"] - prev_info["x"], landmark_info["y"] - prev_info["y"], landmark_info["z"] - prev_info["z"]
            
            movement_direction = ""
            if abs(dx) > 0.01:
                movement_direction += "Left " if dx < 0 else "Right "
            if abs(dy) > 0.05:
                movement_direction += "Up " if dy < 0 else "Down "
            if abs(dz) > 0.1:
                movement_direction += "Backward " if dz < 0 else "Forward "
            
            if movement_direction:
                print(f"{landmark_name} movement: {movement_direction}")

def main():
    args = parse_args()
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    landmark_data_list = []

    net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

    cap = cv.VideoCapture(args.input)

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

if __name__ == "__main__":
    main()
