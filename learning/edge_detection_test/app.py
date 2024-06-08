import cv2
import numpy as np

video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_edge_detection.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 100, 200)
    
    out.write(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))
    
    cv2.imshow('Edge Detection', edges)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
