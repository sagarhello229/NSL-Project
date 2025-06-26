import sys
import cv2
import numpy as np
import requests
from cvzone.HandTrackingModule import HandDetector
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal
import tempfile
import pygame
import threading 

SERVER_URL = "http://127.0.0.1:5000"

class SignLanguageApp(QWidget):
    update_text_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nepali Sign Language Recognition")
        self.setFixedSize(700, 700)

        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFixedHeight(100)
        self.result_text.setStyleSheet("font-size: 18px; color: green;")
        self.update_text_signal.connect(self.result_text.setText)

        self.clear_button = QPushButton("Clear")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.result_text)
        layout.addWidget(self.clear_button)
        self.setLayout(layout)

        self.clear_button.clicked.connect(self.clear_text)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33) 

        pygame.mixer.init()
        self.detector = HandDetector(maxHands=1, detectionCon=0.7)
        self.accumulated_text = ""
        self.last_label = ""
        self.last_spoken_label = ""
        self.confidence_threshold = 0.5
        self.prediction_buffer = []
        self.buffer_size = 3

        self.cooldown_frames = 0
        self.COOLDOWN_LIMIT = 30  

        self.frame_count = 0
        self.frame_skip = 3

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.update_text_signal.emit("Cannot read camera frame.")
            return

        hands, annotated_img = self.detector.findHands(frame, draw=True)

        # if not hands:
        #     self.update_text_signal.emit("No hand detected.")
        #     self.prediction_buffer.clear()
        # else:
        #     self.update_text_signal.emit("")  

        rgb_image = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        # bytes_per_line = ch * w
        # qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # self.image_label.setPixmap(QPixmap.fromImage(qt_image))
        qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

        self.current_frame = frame
        if self.frame_count % self.frame_skip == 0:
            self.auto_predict(hands)

    def auto_predict(self, hands):
        if self.current_frame is None or not hands:
            self.prediction_buffer.clear()
            return

        if self.cooldown_frames > 0:
            self.cooldown_frames -= 1
            return

        hand = hands[0]
        x, y, w, h = hand['bbox']
        margin = 20
        x1 = max(x - margin, 0)
        y1 = max(y - margin, 0)
        x2 = min(x + w + margin, self.current_frame.shape[1])
        y2 = min(y + h + margin, self.current_frame.shape[0])
        hand_img = self.current_frame[y1:y2, x1:x2]

        if hand_img.size == 0:
            self.update_text_signal.emit("Empty hand image.")
            return

        _, img_encoded = cv2.imencode('.jpg', hand_img)
        files = {'image': ('capture.jpg', img_encoded.tobytes(), 'image/jpeg')}

        try:
            response = requests.post(f"{SERVER_URL}/predict", files=files, timeout=5)
            if response.status_code == 200:
                data = response.json()
                label = data.get('label')
                confidence = data.get('confidence', 0)

                if label is None or confidence < self.confidence_threshold:
                    self.prediction_buffer.clear()
                    return

                label = label.strip()

                self.prediction_buffer.append(label)
                if len(self.prediction_buffer) > self.buffer_size:
                    self.prediction_buffer.pop(0)

                if len(self.prediction_buffer) == self.buffer_size and len(set(self.prediction_buffer)) == 1:
                    stable_label = self.prediction_buffer[-1]
                    if stable_label != self.last_label:
                        self.accumulated_text += stable_label + " "
                        self.last_label = stable_label

                        if stable_label != self.last_spoken_label:
                            self.last_spoken_label = stable_label
                            self.result_text.setText(self.accumulated_text)
                            self.cooldown_frames = self.COOLDOWN_LIMIT
                            threading.Thread(target=self.speak_text, args=(stable_label), daemon=True).start()

                    self.prediction_buffer.clear()
            else:
                self.update_text_signal.emit(f"Error: {response.text}")
        except requests.exceptions.Timeout:
            self.update_text_signal.emit("Prediction request timed out.")
        except Exception as e:
            self.update_text_signal.emit(f"Request failed: {str(e)}")

    def speak_text(self, label, silent=False):
        text = label.strip()
        if not text:
            if not silent:
                self.update_text_signal.emit("No recognized text to speak.")
            return
        try:
            response = requests.post(f"{SERVER_URL}/speak", json={"text": text})
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(response.content)
                    audio_path = f.name
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
            else:
                if not silent:
                    self.update_text_signal.emit(f"Error in speech API: {response.text}")
        except Exception as e:
            if not silent:
                self.update_text_signal.emit(f"Request failed: {str(e)}")

    def clear_text(self):
        self.accumulated_text = ""
        self.last_label = ""
        self.last_spoken_label = ""
        self.prediction_buffer.clear()
        self.result_text.clear()

    def closeEvent(self, event):
        self.cap.release()
        pygame.mixer.quit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SignLanguageApp()
    window.show()
    sys.exit(app.exec_())