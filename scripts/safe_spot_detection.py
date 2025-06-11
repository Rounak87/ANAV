import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
import os

# Load DeepLabV3 Model
model = models.segmentation.deeplabv3_resnet101(weights='DEFAULT')
model.eval()


script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the cropped image (30x40 feet area)
image_path = os.path.join(script_dir, "../outputs/cropped_area.jpg")

if not os.path.exists(image_path):
    print(f"❌ Error: Cropped image not found at {image_path}. Ensure `detect_boundary.py` ran successfully.")
    exit()

image = Image.open(image_path).convert("RGB")


preprocess = transforms.Compose([
    transforms.Resize((513, 513)),  # Resize for model input
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
input_tensor = preprocess(image).unsqueeze(0)

# Run DeepLabV3 model
with torch.no_grad():
    output = model(input_tensor)['out'][0]
segmentation_map = torch.argmax(output, dim=0).numpy()

# Save segmentation map
output_path = os.path.join(script_dir, "../outputs/segmentation_map.npy")
np.save(output_path, segmentation_map)
print("Segmentation completed. Safe spots identified.")
