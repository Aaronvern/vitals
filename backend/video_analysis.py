import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
from config import WORKOUTS_COLLECTION_ID
from database import create_document

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
    reps = 1 if knee_angle < 100 else 0  # Simplified rep counting
    return {"reps": reps, "form": form_feedback}

async def analyze_video(file: UploadFile, user: dict):
    video_data = await file.read()
    cap = cv2.VideoCapture()
    cap.open(cv2.imdecode(np.frombuffer(video_data, np.uint8), cv2.IMREAD_COLOR))
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
    workout = create_document(
        WORKOUTS_COLLECTION_ID,
        {
            "user_id": user["$id"],
            "date": datetime.now().isoformat(),
            "reps": total_reps,
            "form_score": 1.0 if "Good" in form_feedback else 0.5,
            "calories": total_reps * 10
        }
    )
    return {
        "user_id": user["$id"],
        "reps": total_reps,
        "form_feedback": form_feedback,
        "calories": total_reps * 10
    }