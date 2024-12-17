import os
import torch
import io
import torchvision.models as models
from fastapi import FastAPI, File, UploadFile
import torchvision.transforms as transforms
from PIL import Image
import logging
os.environ["http_proxy"] = "172.17.0.1:7891"
os.environ["https_proxy"] = "172.17.0.1:7891"
os.environ["TORCH_HOME"] = "./model"
logging.debug("download yolov5s")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
 
# Images
for f in 'zidane.jpg', 'bus.jpg':
    torch.hub.download_url_to_file('https://ultralytics.com/images/' + f, f)  # download 2 images
im1 = Image.open('zidane.jpg')  # PIL image
im2 = cv2.imread('bus.jpg')[..., ::-1]  # OpenCV image (BGR to RGB)
 
# Inference
results = model([im1, im2], size=640) # batch of images
 
# Results
results.print()  
results.save()  # or .show()
 
results.xyxy[0]  # im1 predictions (tensor)
results.pandas().xyxy[0]  # im1 predictions (pandas)