import cv2

#default camera on garne
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Cannot open webcam")
    exit()

while True:
    ret, frame = cam.read()  # euta frame read garne
    if not ret:
        print("Failed to capture frame")
        break

#frame lai dekhune
    cv2.imshow('Real-Time Video', frame)

#press q to exit 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#resource lai free xadne ra window close garne
cam.release()
cv2.destroyAllWindows()