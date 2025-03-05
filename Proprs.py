import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained anti-spoofing model
model = load_model("anti_spoofing_model.h5")

# Function to preprocess frame
def preprocess_frame(frame):
    frame = cv2.resize(frame, (160, 160))  # Resize to model input size
    frame = frame.astype("float") / 255.0  # Normalize
    frame = np.expand_dims(frame, axis=0)  # Add batch dimension
    return frame

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocess frame
    processed_frame = preprocess_frame(frame)
    
    # Predict spoofing
    prediction = model.predict(processed_frame)[0][0]
    
    # Classify as real or fake
    label = "Real" if prediction < 0.5 else "Spoof"
    color = (0, 255, 0) if prediction < 0.5 else (0, 0, 255)

    # Display result
    cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("AI Anti-Spoofing", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
