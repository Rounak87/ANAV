import os

print("🚀 Starting Safe Spot Detection Process...")

os.system("python scripts/detect_boundary.py")
os.system("python scripts/safe_spot_detection.py")
os.system("python scripts/extract_safe_spots.py")

print("✅ Process Completed. Check Outputs Folder.")
