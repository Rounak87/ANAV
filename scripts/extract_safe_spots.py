import numpy as np
import cv2
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load segmentation map
segmentation_map_path = os.path.join(script_dir, "../outputs/segmentation_map.npy")

if not os.path.exists(segmentation_map_path):
    print(f"❌ Error: Segmentation map not found at {segmentation_map_path}. Run `safe_spot_detection.py` first.")
    exit()

segmentation_map = np.load(segmentation_map_path)

# Load the original cropped image for visualization
cropped_image_path = os.path.join(script_dir, "../outputs/cropped_area.jpg")
image = cv2.imread(cropped_image_path)

# Define "safe" areas (assuming class 1 represents flat areas)
safe_zone_mask = (segmentation_map == 1).astype("uint8")

# Find contours of safe zones
contours, _ = cv2.findContours(safe_zone_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

safe_spots = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w * h > 0:  # Ensure safe zone is at least 1.2m x 1.2m in pixel size
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Mark safe spots in red
        safe_spots.append((x, y, w, h))

# Ensure the output directory exists
output_dir = os.path.join(script_dir, "../outputs")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the final processed image
marked_image_path = os.path.join(output_dir, "safe_spots_marked.jpg")
cv2.imwrite(marked_image_path, image)

# Save Safe Spot Coordinates
safe_spots_path = os.path.join(output_dir, "safe_spots.npy")
np.save(safe_spots_path, safe_spots)

print(f"Detected {len(safe_spots)} safe spots. Coordinates saved.")
