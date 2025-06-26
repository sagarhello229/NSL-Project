# import sys
# import cv2
# import numpy as np
# import requests
# from cvzone.HandTrackingModule import HandDetector
# from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import QTimer
# import tempfile
# import pygame

# SERVER_URL = "http://127.0.0.1:5000"

# class SignLanguageApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Nepali Sign Language Recognition")
#         self.setFixedSize(700, 700)

#         self.image_label = QLabel()
#         self.image_label.setFixedSize(640, 480)

#         self.result_text = QTextEdit()
#         self.result_text.setReadOnly(True)
#         self.result_text.setFixedHeight(100)
#         self.result_text.setStyleSheet("font-size: 18px; color: green;")

#         self.speak_button = QPushButton("Speak")
#         self.clear_button = QPushButton("Clear")

#         layout = QVBoxLayout()
#         layout.addWidget(self.image_label)
#         layout.addWidget(self.result_text)
#         layout.addWidget(self.speak_button)
#         layout.addWidget(self.clear_button)
#         self.setLayout(layout)

#         self.speak_button.clicked.connect(self.speak_text)
#         self.clear_button.clicked.connect(self.clear_text)

#         self.cap = cv2.VideoCapture(0)
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(30)

#         pygame.mixer.init()
#         self.detector = HandDetector(maxHands=1, detectionCon=0.7)
#         self.accumulated_text = ""
#         self.last_label = ""
#         self.confidence_threshold = 0.7
#         self.prediction_buffer = []
#         self.buffer_size = 3

#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if ret:
#             hands, annotated_img = self.detector.findHands(frame, draw=True)

#             rgb_image = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
#             h, w, ch = rgb_image.shape
#             bytes_per_line = ch * w
#             qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#             self.image_label.setPixmap(QPixmap.fromImage(qt_image))
#             self.current_frame = frame
#             self.auto_predict(hands)

#     def auto_predict(self, hands):
#         if not hasattr(self, 'current_frame') or self.current_frame is None:
#             return

#         if not hands:
#             print("No hand detected.")
#             self.prediction_buffer.clear()
#             return

#         hand = hands[0]
#         x, y, w, h = hand['bbox']
#         margin = 20
#         x1 = max(x - margin, 0)
#         y1 = max(y - margin, 0)
#         x2 = min(x + w + margin, self.current_frame.shape[1])
#         y2 = min(y + h + margin, self.current_frame.shape[0])
#         hand_img = self.current_frame[y1:y2, x1:x2]

#         if hand_img.size == 0:
#             print("Empty hand image.")
#             return

#         _, img_encoded = cv2.imencode('.jpg', hand_img)
#         files = {'image': ('capture.jpg', img_encoded.tobytes(), 'image/jpeg')}

#         try:
#             response = requests.post(f"{SERVER_URL}/predict", files=files, timeout=5)
#             if response.status_code == 200:
#                 data = response.json()
#                 label = data.get('label', '').strip()
#                 confidence = data.get('confidence', 0)

#                 print(f"Predicted: '{label}' with confidence {confidence:.4f}")

#                 if confidence < self.confidence_threshold or not label:
#                     self.prediction_buffer.clear()
#                     return

#                 self.prediction_buffer.append(label)
#                 if len(self.prediction_buffer) > self.buffer_size:
#                     self.prediction_buffer.pop(0)

#                 if len(self.prediction_buffer) == self.buffer_size and len(set(self.prediction_buffer)) == 1:
#                     stable_label = self.prediction_buffer[-1]
#                     if stable_label != self.last_label:
#                         self.accumulated_text += stable_label + " "
#                         self.last_label = stable_label
#                         self.result_text.setText(self.accumulated_text)
#                     self.prediction_buffer.clear()
#             else:
#                 self.result_text.setText(f"Error: {response.text}")
#         except requests.exceptions.Timeout:
#             print("Prediction request timed out.")
#         except Exception as e:
#             self.result_text.setText(f"Request failed: {str(e)}")

#     def speak_text(self):
#         if not self.accumulated_text.strip():
#             self.result_text.setText("No recognized text to speak.")
#             return
#         try:
#             response = requests.post(f"{SERVER_URL}/speak", json={"text": self.accumulated_text})
#             if response.status_code == 200:
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
#                     f.write(response.content)
#                     audio_path = f.name
#                 pygame.mixer.music.load(audio_path)
#                 pygame.mixer.music.play()
#             else:
#                 self.result_text.setText(f"Error in speech API: {response.text}")
#         except Exception as e:
#             self.result_text.setText(f"Request failed: {str(e)}")

#     def clear_text(self):
#         self.accumulated_text = ""
#         self.last_label = ""
#         self.prediction_buffer.clear()
#         self.result_text.clear()

#     def closeEvent(self, event):
#         self.cap.release()
#         pygame.mixer.quit()
#         event.accept()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = SignLanguageApp()
#     window.show()
#     sys.exit(app.exec_())

# import os
# import hashlib
# import cv2

# def dhash(image, hashSize=8):
#     # Simple image hashing function for duplicate detection
#     import cv2
#     resized = cv2.resize(image, (hashSize + 1, hashSize))
#     diff = resized[:, 1:] > resized[:, :-1]
#     return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

# image_hashes = {}
# duplicates = []

# for root, dirs, files in os.walk('/home/sagar/Code/project-3/nsl_dataset/combined_dataset/ह'):
#     for file in files:
#         path = os.path.join(root, file)
#         img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             continue
#         h = dhash(img)
#         if h in image_hashes:
#             duplicates.append(path)
#         else:
#             image_hashes[h] = path

# print(f"Found duplicates: {duplicates}")
# print(f"Total duplicate images found: {len(duplicates)}")

# for file_path in duplicates:
#     try:
#         os.remove(file_path)
#         print(f"Deleted duplicate: {file_path}")
#     except Exception as e:
#         print(f"Error deleting {file_path}: {e}")




# from PIL import Image
# import os

# corrupted_files = []

# for filename in os.listdir('/home/sagar/Code/project-3/nsl_dataset/combined_dataset/क्ष'):
#     path = os.path.join('/home/sagar/Code/project-3/nsl_dataset/combined_dataset/क्ष', filename)
#     try:
#         img = Image.open(path)
#         img.verify()  # verify does not load full image but checks integrity
#     except (IOError, SyntaxError) as e:
#         corrupted_files.append(path)

# print("Corrupted files:", corrupted_files)
# # Remove or fix these files


# import cv2
# import os

# def is_blurry(image_path, threshold=100):
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if image is None:
#         print(f"Could not read image: {image_path}")
#         return True  # Treat unreadable images as blurry
#     laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
#     return laplacian_var < threshold

# blurry_images = []

# imagePath = '/home/sagar/Code/project-3/nsl_dataset/combined_dataset/क'

# for file in os.listdir(imagePath):  
#     path = os.path.join(imagePath, file) 
#     if is_blurry(path):
#         blurry_images.append(path)

# print("Blurry images:", blurry_images)
# print(f"Total blurry images found: {len(blurry_images)}")




# import cv2
# import os
# import numpy as np

# def is_blurry(image_path, threshold=100):
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if image is None:
#         return True
#     laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
#     return laplacian_var < threshold

# def unsharp_mask(image, ksize=(5, 5), sigma=1.0, strength=1.5):
#     blurred = cv2.GaussianBlur(image, ksize, sigma)
#     sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
#     return sharpened

# # Folder containing original images
# folder = '/home/sagar/Code/project-3/nsl_dataset/combined_dataset/ह'

# for file in os.listdir(folder):
#     path = os.path.join(folder, file)

#     if is_blurry(path):
#         image = cv2.imread(path)
#         if image is None:
#             print(f" Could not read {file}")
#             continue

#         enhanced = unsharp_mask(image)
#         cv2.imwrite(path, enhanced) 
#         print(f" Enhanced and replaced: {file}")
#     else:
#         print(f" Not blurry: {file}")




