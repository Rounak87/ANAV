import cv2
import numpy as np
import os

#loading the image here
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "../images/test_image2.jpg")

if not os.path.exists(image_path):
    print(f"Error: Image file not found at {image_path}. Please check the file path.")
    exit()

image = cv2.imread(image_path)
if image is None:
    print("Error: Unable to read the image. Check the file format and path.")
    exit()

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Converting to HSV

# Define the range for detecting yellow color
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# findind contours of the yellow boundary
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# working on the largest detected contour
if contours:
    largest_contour = max(contours, key=cv2.contourArea)  # Select the biggest detected area
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Crop the detected yellow area
    cropped_image = image[y:y+h, x:x+w]
    
    output_dir = os.path.join(script_dir, "../outputs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, "cropped_area.jpg")
    cv2.imwrite(output_path, cropped_image)

    print(f"Yellow boundary detected at ({x}, {y}, {w}, {h})")
else:
    print("No yellow boundary detected.")
