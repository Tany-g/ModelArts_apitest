import torch
import os
import cv2
import pandas
os.environ["TORCH_HOME"] = "./model"
# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom
 
# Images
img = "https://ultralytics.com/images/zidane.jpg"  # or file, Path, PIL, OpenCV, numpy, list
 
# Inference
results = model(img)
results.save("test.jpg")
# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.