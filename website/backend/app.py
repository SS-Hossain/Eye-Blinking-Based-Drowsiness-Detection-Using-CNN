# === backend/app.py ===

from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from keras.models import load_model
import time
import threading
import os
import pygame

# Setup
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
pygame.mixer.init()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load model and cascades
model = load_model('Fold_0.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Globals
capture = None
drowsy_start_time = None
drowsy_duration_threshold = 1.6
alarm_audio_path = 'alarm-sound.mp3'
alarm_triggered = False


def play_alarm():
    global alarm_triggered
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(alarm_audio_path)
        pygame.mixer.music.play(-1)
        alarm_triggered = True


def detect_drowsiness():
    global capture, drowsy_start_time, alarm_triggered
    while True:
        if not capture:
            continue

        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        drowsy_status = "Drowsy"

        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            face_region = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(face_region, 1.1, 5, minSize=(30, 30))

            if len(eyes) >= 2:
                min_x, max_x = min(eyes[0][0], eyes[1][0]), max(eyes[0][0]+eyes[0][2], eyes[1][0]+eyes[1][2])
                min_y, max_y = min(eyes[0][1], eyes[1][1]), max(eyes[0][1]+eyes[0][3], eyes[1][1]+eyes[1][3])
                eyes_region = gray[y + min_y:y + max_y, x + min_x:x + max_x]

                if eyes_region.size > 0:
                    preprocessed_img = cv2.resize(eyes_region, (150, 60)) / 255.0
                    input_img = np.expand_dims(preprocessed_img, axis=(0, -1))
                    pred = np.argmax(model.predict(input_img), axis=1)[0]
                    label_map = {0: "Not Drowsy", 1: "Drowsy"}
                    drowsy_status = label_map.get(pred, "Drowsy")

        if drowsy_status == "Drowsy":
            if drowsy_start_time is None:
                drowsy_start_time = time.time()
            elif time.time() - drowsy_start_time >= drowsy_duration_threshold and not alarm_triggered:
                threading.Thread(target=play_alarm, daemon=True).start()
        else:
            drowsy_start_time = None

        cv2.putText(frame, f"Status: {drowsy_status}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return "Backend is running."


@app.route('/start')
def start():
    global capture
    if not capture:
        capture = cv2.VideoCapture(0)
    return "Camera started"


@app.route('/stop')
def stop():
    global capture, alarm_triggered, drowsy_start_time
    if capture:
        capture.release()
        capture = None
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    alarm_triggered = False
    drowsy_start_time = None
    return "Camera and alarm stopped"


@app.route('/video_feed')
def video_feed():
    return Response(detect_drowsiness(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/alarm_status')
def alarm_status():
    global alarm_triggered
    return jsonify({"alarm": alarm_triggered})


@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    global alarm_triggered, drowsy_start_time
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    alarm_triggered = False
    drowsy_start_time = None
    return "Alarm stopped"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
