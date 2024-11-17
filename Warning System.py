import cv2
import numpy as np
import time
from ultralytics import YOLO

# Load YOLOv8 model (you could replace this with YOLOv10 if using a compatible version)
model = YOLO("yolov8n.pt")  # Use "yolov10n.pt" for YOLOv10, if available

# Define parameters for collision warning
DISTANCE_THRESHOLD = 30  # Threshold distance in meters (to be tuned)
TTC_THRESHOLD = 3  # Time-to-collision threshold in seconds
FRAME_RATE = 30  # Assuming 30 frames per second

# Function to calculate relative speed (dummy implementation)
def calculate_relative_speed():
    # Placeholder - replace with actual sensor data or calculations
    return 10  # m/s

# Calculate time-to-collision (TTC) based on distance and relative speed
def calculate_ttc(distance, speed):
    if speed > 0:
        return distance / speed
    return float('inf')  # Infinite time if speed is zero

# Start video feed (or load video file)
video_source = "path_to_video.mp4"  # Replace with 0 for webcam
cap = cv2.VideoCapture(video_source)

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if no frame is retrieved

    # Resize frame for faster processing
    frame_resized = cv2.resize(frame, (640, 640))

    # Perform object detection
    results = model(frame_resized)

    # Parse detection results
    for detection in results:
        x1, y1, x2, y2, conf, cls = detection.xyxy[0]  # Coordinates and confidence

        # Assuming 'car' class is represented by index 2 (adjust as per model's labels)
        if cls == 2:  # Only consider 'car' objects
            # Calculate distance based on bounding box size (dummy example)
            distance = 50 * (1 - conf)  # Placeholder calculation

            # Calculate relative speed and time-to-collision
            speed = calculate_relative_speed()
            ttc = calculate_ttc(distance, speed)

            # Display bounding box and label
            label = f"Car, Distance: {distance:.2f}m, TTC: {ttc:.2f}s"
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Collision warning logic
            if distance < DISTANCE_THRESHOLD and ttc < TTC_THRESHOLD:
                print("Warning: Potential Collision Detected!")
                # Trigger braking system (simulation)
                cv2.putText(frame, "BRAKE!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    # Display the output frame
    cv2.imshow("Forward Collision Warning", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Press 'q' to quit

cap.release()
cv2.destroyAllWindows()
