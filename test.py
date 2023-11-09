#pip install mediapipe opencv-python

import cv2
import mediapipe as mp
import numpy as np
import sys


#everything that lets the drawing happen
mp_drawing = mp.solutions.drawing_utils
#selecting the model for pose detection
mp_pose = mp.solutions.pose

args = sys.argv

if len(args) == 1:
    args.append(0)

"""just to ge thte video feed"""
# #get the video feed
# cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     ret, frame = cap.read()
#     #puts a pop up on our screen of what the feed is
#     cv2.imshow('Mediapipe Feed', frame)

#     #check if the window is closed or q is pressed
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
# #releases the webcam
# cap.release()
# #closes the video feed
# cv2.destroyAllWindows()

"""using media pipe to get the objects"""
# #start applying media pipe
# #get the video feed
# cap = cv2.VideoCapture(0)
# #setup mp
# # min_detection_confidence = how accurate is the detection
# # min_tracking_confidence = maintaining tracking state
# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#     while cap.isOpened():
#         ret, frame = cap.read()

#         #detect pose and render
#         #recolor image to RGB
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False

#         #making the detection
#         results = pose.process(image)

#         #recolor back to BGR
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         #prints out the results, but doesn't render anything
#         print(results)

#         #puts a pop up on our screen of what the feed is
#         cv2.imshow('Mediapipe Feed', frame)

#         #check if the window is closed or q is pressed
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
# #releases the webcam
# cap.release()
# #closes the video feed
# cv2.destroyAllWindows()

"""render"""
# #start applying media pipe
# #get the video feed
# cap = cv2.VideoCapture(0)
# #setup mp
# # min_detection_confidence = how accurate is the detection
# # min_tracking_confidence = maintaining tracking state
# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#     while cap.isOpened():
#         ret, frame = cap.read()

#         #detect pose and render
#         #recolor image to RGB
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False

#         #making the detection
#         results = pose.process(image)

#         #recolor back to BGR
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         #render detections
#         mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#         #puts a pop up on our screen of what the feed is
#         cv2.imshow('Mediapipe Feed', image)

#         #check if the window is closed or q is pressed
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
# #releases the webcam
# cap.release()
# #closes the video feed
# cv2.destroyAllWindows()

"""change the colors"""
# #start applying media pipe
# #get the video feed
# cap = cv2.VideoCapture(args[1])
# #setup mp
# # min_detection_confidence = how accurate is the detection
# # min_tracking_confidence = maintaining tracking state
# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#     while cap.isOpened():
#         ret, frame = cap.read()

#         #detect pose and render
#         #recolor image to RGB
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False

#         #making the detection
#         results = pose.process(image)

#         #recolor back to BGR
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         #render detections
#         mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                   mp_drawing.DrawingSpec(color=(255,0,255), thickness=2, circle_radius=2), 
#                                   mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2))

#         #puts a pop up on our screen of what the feed is
#         cv2.imshow('Mediapipe Feed', image)

#         #check if the window is closed or q is pressed
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
# #releases the webcam
# cap.release()
# #closes the video feed
# cv2.destroyAllWindows()

"""Getting all the joints"""
#start applying media pipe
#get the video feed
cap = cv2.VideoCapture(args[1])
#setup mp
# min_detection_confidence = how accurate is the detection
# min_tracking_confidence = maintaining tracking state
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        #detect pose and render
        #recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        #making the detection
        results = pose.process(image)

        #recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #get the landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            print(landmarks)
        except:
            pass



        #render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255,0,255), thickness=2, circle_radius=2), 
                                  mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2))

        #puts a pop up on our screen of what the feed is
        cv2.imshow('Mediapipe Feed', image)

        #check if the window is closed or q is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
#releases the webcam
cap.release()
#closes the video feed
cv2.destroyAllWindows()

#len(landmarks)
#for landmrk in mp_pose.PoseLandmark:
#   print(landmrk)

#landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]