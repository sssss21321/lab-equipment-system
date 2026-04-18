"""
实验室设备管理系统 - 生产环境入口
FastAPI 同时托管前端静态文件和后端 API
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from app.main import app as fastapi_app

# 托管前端静态文件
fastapi_app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

@fastapi_app.get("/")
async def root():
    return FileResponse("dist/index.html")

@fastapi_app.get("/{path:path}")
async def spa(path: str):
    file_path = f"dist/{path}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse("dist/index.html")

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
