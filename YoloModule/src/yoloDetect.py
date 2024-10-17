import cv2
import json
import time
import os
import logging
from datetime import datetime
from ultralytics import YOLO
import requests
import mysql.connector  

# Setup logging
logging.basicConfig(
    filename='C:/Users/masmu/OneDrive/Documents/Magang - Lab SI/YoloDashboard/YoloDashboardTest/YoloModule/logs/yolo.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Konfigurasi MySQL
db_config = {
    'user': 'root',
    'password': '',  
    'host': 'localhost',
    'database': 'yolodetect'
}

# Membuat koneksi ke MySQL
try:
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    print("Koneksi berhasil!")
except mysql.connector.Error as err:
    logging.error(f"Error: {err}")
    exit(1)  # Menghentikan skrip jika tidak bisa terhubung ke database

# Konfigurasi YOLO dan Deteksi
MODEL_PATH = 'src/yolov8s.pt'
SAVE_INTERVAL = 10 # Interval waktu untuk menyimpan data deteksi (5 menit)
DETECTION_INTERVAL = 1  # Interval deteksi dalam detik (1 detik)
API_ENDPOINT = 'http://localhost:3000/api/detections'  # Endpoint backend untuk mengirim data

# Initialize YOLOv8 model
model = YOLO(MODEL_PATH)

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    logging.error("Tidak bisa mengakses webcam.")
    exit(1)

people_count = 0
detection_summary = {}
start_time = time.time()
save_time = start_time  # Variabel baru untuk mengatur interval penyimpanan data

logging.info("Deteksi dimulai.")

while True:
    ret, frame = cap.read()
    if not ret:
        logging.error("Tidak bisa membaca frame dari webcam.")
        break

    # Perform object detection every DETECTION_INTERVAL seconds
    if time.time() - start_time >= DETECTION_INTERVAL:
        # Reset the start time for the next detection
        start_time = time.time()

        # Perform object detection
        results = model(frame)

        # Process detection results
        frame_people_count = 0

        for r in results:
            for box in r.boxes:
                cls = r.names[int(box.cls[0])]
                conf = box.conf[0].item()  # Konversi tensor menjadi float serta Ambil confidence score
                if cls == "person":
                    frame_people_count += 1

                # Akumulasi informasi deteksi
                if cls in detection_summary:
                    detection_summary[cls] += 1
                else:
                    detection_summary[cls] = 1

                logging.info(f"Deteksi objek '{cls}' dengan confidence {conf}.")

                # Extract coordinates for cv2 functions
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()

                # Draw the bounding box and label
                cv2.putText(frame, f'{cls} ({conf:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (36, 255, 12), 2)

        # Jumlah people count
        people_count += frame_people_count

        # Tampilkan frame
        cv2.imshow('YOLOv8 Detection', frame)

    # Simpan hasil deteksi setiap 5 menit
    if time.time() - save_time > SAVE_INTERVAL:
        # Simpan ke SQL
        try:
            for label, count in detection_summary.items():
                cursor.execute("""
                    INSERT INTO detections (label, confidence, timestamp, total_people_count)
                    VALUES (%s, %s, %s, %s)
                """, (label, conf, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), count))
            db_connection.commit()
            logging.info("Data akumulasi berhasil disimpan ke database MySQL.")
        except mysql.connector.Error as e:
            logging.error(f"Error saat menyimpan data ke MySQL: {e}")
            db_connection.rollback()

        # Clear data akumulasi dan reset waktu (setiap 5 menit)
        detection_summary = {}
        people_count = 0
        save_time = time.time()  # Reset waktu

    # Exit program saat tekan 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        logging.info("Deteksi dihentikan oleh pengguna.")
        break

cap.release()
cv2.destroyAllWindows()
cursor.close()
db_connection.close()
logging.info("Deteksi berakhir.")
