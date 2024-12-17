import os
import torch
import io
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from time import time
import numpy as np
import logging
from fastapi.responses import StreamingResponse,FileResponse,JSONResponse
import hashlib
logger = logging.getLogger("debug")
logger.setLevel(logging.DEBUG)
# 设置环境变量，用于指定模型和权重文件的存储位置
os.environ["TORCH_HOME"] = "./model"
logging.debug("load model")
# 加载YOLOv5模型
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

logging.debug("download yolov5s")
model = torch.hub.load(
            "./model/hub/ultralytics_yolov5_master",
            "custom",
            path="./yolov5s.pt",
            device="cpu",
            source='local',
            _verbose=True,
        )


app = FastAPI()

@app.post("/")
async def detect_objects(file: UploadFile = File(...)):
    # 将上传的文件转换为PIL图像
    file_content = await file.read()
    image_name = hashlib.sha256(file_content).hexdigest()
    image = Image.open(io.BytesIO(file_content))
    
    # 将PIL图像转换为OpenCV图像
    image = np.array(image)
    
    # 将BGR格式转换为RGB格式
    # image = image[..., ::-1]
    
    logging.debug("starting detect......")
    # 进行目标检测
    results = model(image, size=640)
    # results.save("s.jpeg")

    results.render()  # updates results.ims with boxes and labels
    im = results.ims[0]
    img = Image.fromarray(im)
    buffer = io.BytesIO()
    img.save(f"results/{image_name}.jpeg", format='jpeg')
    # img_byte_arr = img_byte_arr.getvalue()
    return FileResponse(path=f"results/{image_name}.jpeg", media_type="image/jpeg", filename="a.jpeg")

@app.post("/json")
async def detect_objects(file: UploadFile = File(...)):
    # 将上传的文件转换为PIL图像
    file_content = await file.read()
    image = Image.open(io.BytesIO(file_content))
    
    # 将PIL图像转换为OpenCV图像
    image = np.array(image)
    
    # 将BGR格式转换为RGB格式
    # image = image[..., ::-1]
    
    logging.debug("starting detect......")
    # 进行目标检测
    results = model(image, size=640)
    # results.save("s.jpeg")

    results_df = results.pandas().xyxy[0]
    
    # 将DataFrame转换为JSON格式
    results_json = results_df.to_dict(orient="records")
    
    # 返回JSON响应
    return JSONResponse(content=results_json)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)