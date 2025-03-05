import cv2
import numpy as np
from model import load_model

# Load AI model
try:
    model = load_model()
except Exception as e:
    print("Error loading model:", str(e))
    exit()

# Load OpenCV face detector once
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access webcam.")
    exit()

def preprocess_face(face):
    """Resize, normalize, and expand dimensions for model input."""
    face_resized = cv2.resize(face, (128, 128))
    face_normalized = face_resized.astype("float32") / 255.0  # Normalize
    return np.expand_dims(face_normalized, axis=0)  # Add batch dimension

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]  # Extract face region

        # Ensure face detection area is valid
        if face.shape[0] == 0 or face.shape[1] == 0:
            continue

        # Preprocess face
        face_input = preprocess_face(face)

        # Predict spoofing
        prediction = model.predict(face_input)[0][0]

        # Set label and color
        label = "Real Face" if prediction > 0.5 else "Fake Face"
        color = (0, 255, 0) if prediction > 0.5 else (0, 0, 255)

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Display output
    cv2.imshow("Face Anti-Spoofing", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
