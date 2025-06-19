import sys
import cv2
import numpy as np
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import tempfile
import pygame

SERVER_URL = "http://127.0.0.1:5000"

class SignLanguageApp(QWidget):
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

        self.speak_button = QPushButton("Speak")
        self.clear_button = QPushButton("Clear")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.result_text)
        layout.addWidget(self.speak_button)
        layout.addWidget(self.clear_button)
        self.setLayout(layout)

        self.speak_button.clicked.connect(self.speak_text)
        self.clear_button.clicked.connect(self.clear_text)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  

        pygame.mixer.init()
        self.accumulated_text = ""
        self.last_label = ""
        self.confidence_threshold = 0.7
        self.prediction_buffer = []
        self.buffer_size = 3  

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qt_image))
            self.current_frame = frame
            self.auto_predict()

    def auto_predict(self):
        if not hasattr(self, 'current_frame') or self.current_frame is None:
            return

        gray = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
        mean_pixel = np.mean(gray)
        std_pixel = np.std(gray)

        if mean_pixel < 20 or std_pixel < 5:
            print(f"Skipped prediction — Mean: {mean_pixel:.2f}, Std: {std_pixel:.2f}")
            self.prediction_buffer.clear()
            return

        _, img_encoded = cv2.imencode('.jpg', self.current_frame)
        files = {'image': ('capture.jpg', img_encoded.tobytes(), 'image/jpeg')}

        try:
            response = requests.post(f"{SERVER_URL}/predict", files=files, timeout=5)
            if response.status_code == 200:
                data = response.json()
                label = data.get('label', '').strip()
                confidence = data.get('confidence', 0)

                print(f"Predicted: '{label}' with confidence {confidence:.4f}")

                if confidence < self.confidence_threshold or not label:
                    self.prediction_buffer.clear()
                    return

                self.prediction_buffer.append(label)
                if len(self.prediction_buffer) > self.buffer_size:
                    self.prediction_buffer.pop(0)

                if len(self.prediction_buffer) == self.buffer_size and len(set(self.prediction_buffer)) == 1:
                    stable_label = self.prediction_buffer[-1]
                    if stable_label != self.last_label:
                        self.accumulated_text += stable_label + " "
                        self.last_label = stable_label
                        self.result_text.setText(self.accumulated_text)
                    self.prediction_buffer.clear()
            else:
                self.result_text.setText(f"Error: {response.text}")
        except requests.exceptions.Timeout:
            print("Prediction request timed out.")
        except Exception as e:
            self.result_text.setText(f"Request failed: {str(e)}")


    def speak_text(self):
        if not self.accumulated_text.strip():
            self.result_text.setText("No recognized text to speak.")
            return
        try:
            response = requests.post(f"{SERVER_URL}/speak", json={"text": self.accumulated_text})
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(response.content)
                    audio_path = f.name
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
            else:
                self.result_text.setText(f"Error in speech API: {response.text}")
        except Exception as e:
            self.result_text.setText(f"Request failed: {str(e)}")

    def clear_text(self):
        self.accumulated_text = ""
        self.last_label = ""
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
