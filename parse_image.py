import cv2 as cv
import numpy as np
import argparse
import mediapipe as mp
import json

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='Path to the input video file or 0 for webcam')
parser.add_argument('--threshold', default=0.2, type=float)
parser.add_argument('--width', default=368, type=int)
parser.add_argument('--height', default=368, type=int)

args = parser.parse_args()
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
landmark_data_list = []


BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

inWidth = args.width
inHeight = args.height

net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

# Initialize video capture (use '0' for webcam or path to video file)
cap = cv.VideoCapture(args.input)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        #detect pose and render
        #recolor image to RGB
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image.flags.writeable = False

        #making the detection
        results = pose.process(image)

        #recolor back to BGR
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        #get the landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            frame_landmark_data = {}
            for landmark, landmark_name in zip(landmarks, mp_pose.PoseLandmark):
                frame_landmark_data[landmark_name.name] = {
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z if landmark.HasField("z") else None,
                }
            landmark_data_list.append(frame_landmark_data)
        except:
            pass

        #render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255,0,255), thickness=2, circle_radius=2), 
                                  mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2))

        #puts a pop up on our screen of what the feed is
        cv.imshow('Mediapipe Feed', image)

        #check if the window is closed or q is pressed
        if cv.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()

for frame_idx, frame_landmark_data in enumerate(landmark_data_list):
    print(f"LANDMARKS - Frame {frame_idx}")
    for landmark_name, landmark_info in frame_landmark_data.items():
        print(landmark_name, "x:", landmark_info["x"], "y:", landmark_info["y"], "z:", landmark_info["z"])
