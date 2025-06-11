import cv2
import numpy as np


lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
threshold_percent = 2  # Lower for thin lines

def yellow_percentage(zone):
    yellow_pixels = cv2.countNonZero(zone)
    total_pixels = zone.size
    return (yellow_pixels / total_pixels) * 100

def detect_boundary_and_corners_custom(mask, threshold_percent=5):
    height, width = mask.shape
    left_end = width // 3
    right_start = width * 2 // 3
    left_zone = mask[:, :left_end]
    middle_zone = mask[:, left_end:right_start]
    right_zone = mask[:, right_start:]  

    left = yellow_percentage(left_zone) > threshold_percent
    middle = yellow_percentage(middle_zone) > threshold_percent
    right = False  

    if left and middle:
        return "Left-Middle Corner detected"
    elif left and not middle:
        return "Boundary detected at left"
    elif middle and not left:
        return "Boundary detected at middle"
    else:
        return "No boundary detected"

def draw_zone_overlay_custom(frame):
    height, width, _ = frame.shape
    left_end = width // 3
    right_start = width * 2 // 3
    cv2.line(frame, (left_end, 0), (left_end, height), (0, 255, 255), 2)
    cv2.line(frame, (right_start, 0), (right_start, height), (0, 255, 255), 2)
    cv2.putText(frame, "Left", (left_end//4, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    cv2.putText(frame, "Middle", (width//2 - 60, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    cv2.putText(frame, "Right", (right_start + (width-right_start)//4, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    return frame

def process_video(video_path, output_path='output_with_overlay.mp4'):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties for writer
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        message = detect_boundary_and_corners_custom(mask, threshold_percent)
        frame = draw_zone_overlay_custom(frame)
        cv2.putText(frame, message, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

       
        out.write(frame)

       

    cap.release()
    out.release()
   

if __name__ == '__main__':
    process_video('newwvid.mp4', 'output_with_overlay.mp4')  
