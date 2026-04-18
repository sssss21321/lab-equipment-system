"""
实验室设备管理系统 - 生产环境入口
FastAPI 同时托管前端静态文件和后端 API
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from app.main import app as fastapi_app

# 托管前端静态文件
frontend_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
assets_dir = os.path.join(frontend_dist, "assets")

if os.path.exists(assets_dir):
    fastapi_app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@fastapi_app.get("/")
async def root():
    index_path = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Lab Equipment API is running", "version": "1.0.0"})

@fastapi_app.get("/health")
async def health():
    """Railway 健康检查端点"""
    return JSONResponse({"status": "ok"})

@fastapi_app.get("/{path:path}")
async def spa(path: str):
    file_path = os.path.join(frontend_dist, path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
