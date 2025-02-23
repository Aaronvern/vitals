import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import tempfile
import os
from config import WORKOUTS_COLLECTION_ID
from database import create_document
from fastapi import UploadFile

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def calculate_angle(p1, p2, p3):
    a = np.array([p1.x, p1.y]) - np.array([p2.x, p2.y])
    b = np.array([p3.x, p3.y]) - np.array([p2.x, p2.y])
    cosine_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    angle = np.degrees(np.arccos(cosine_angle))
    return angle

def analyze_frame(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    if not results.pose_landmarks:
        return {"reps": 0, "form": "No pose detected"}
    landmarks = results.pose_landmarks.landmark
    knee_angle = calculate_angle(landmarks[23], landmarks[25], landmarks[27])  # Hip-Knee-Ankle
    form_feedback = "Good" if 90 < knee_angle < 110 else "Adjust knees"
    reps = 1 if knee_angle < 100 else 0 
    return {"reps": reps, "form": form_feedback}

async def analyze_video(file: UploadFile, user: dict):
    
    video_data = await file.read()
    if not video_data:
        raise ValueError("No video data provided")

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(video_data)
        temp_file_path = temp_file.name

    
    cap = cv2.VideoCapture(temp_file_path)
    if not cap.isOpened():
        os.remove(temp_file_path)  
        raise ValueError("Failed to open video file")

    total_reps = 0
    form_feedback = ""
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result = analyze_frame(frame)
        total_reps += result["reps"]
        form_feedback = result["form"]
    cap.release()

   
    os.remove(temp_file_path)

    
    total_reps = max(1, min(total_reps, 10000)) 
    form_score = 1 if "Good" in form_feedback else 0 
    form_score = max(1, min(form_score, 10000))  

    print(f" voohooo aaron herw Total reps: {total_reps}, Form feedback: {form_feedback}, Form score: {form_score}")

    workout = create_document(
        WORKOUTS_COLLECTION_ID,
        {
            "user_id": user["$id"],
            "date": datetime.now().isoformat(),
            "reps": total_reps,
            "form_score": form_score, 
            "calories": total_reps * 10
        }
    )
    return {
        "user_id": user["$id"],
        "reps": total_reps,
        "form_feedback": form_feedback,
        "calories": total_reps * 10
    }