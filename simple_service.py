from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
app = FastAPI()

@app.post("/")
async def create_upload_file(image: UploadFile = File(...)):
    # 读取文件内容
    content = await image.read()
    
    # 获取或设置文件名
    filename = image.filename
    
    # 设置响应头以包含文件名信息
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    
    # 确定媒体类型 (MIME 类型)
    media_type = "image/jpeg"  # 默认值，可以根据需要更改
    if image.content_type:
        media_type = image.content_type
    
    # 使用 BytesIO 创建一个可迭代的文件对象
    file_like_object = BytesIO(content)
    
    # 返回 StreamingResponse 以直接流式传输图片
    return StreamingResponse(file_like_object, media_type=media_type, headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)