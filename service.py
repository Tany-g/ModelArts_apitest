import os
import torch
import io
import torchvision.models as models
from fastapi import FastAPI, File, UploadFile
import torchvision.transforms as transforms
from PIL import Image

# os.environ["http_proxy"] = "172.28.224.1:7890"
# os.environ["https_proxy"] = "172.28.224.1:7890"
os.environ["TORCH_HOME"] = "./model"
resnet18 = models.resnet18(pretrained=True)
resnet18.eval()
# 图像变换
transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def load_class_names(file_path):
    with open(file_path, "r") as f:
        class_names = [line.strip() for line in f.readlines()]
    return class_names


class_names = load_class_names("label.txt")

app = FastAPI()


@app.post("/")
async def classify_image(file: UploadFile = File(...)):
    # 将上传的文件转换为PIL图像
    image = Image.open(io.BytesIO(await file.read()))

    # 使用之前定义的transform对图像进行预处理
    image_tensor = transform(image).unsqueeze(0)

    # 将图像传递给模型进行预测
    with torch.no_grad():
        output = resnet18(image_tensor)
        _, predicted = torch.max(output, 1)

    # 返回预测的类别索引

    return {"predicted_class": class_names[predicted.item()]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
