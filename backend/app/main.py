# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models  # 必须导入，注册所有模型到 Base.metadata
from app.routers import equipment, usage

app = FastAPI(title="Lab Equipment API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Lab Equipment API is running", "version": "1.0.0"}

app.include_router(equipment.router, prefix="/api/equipment", tags=["Equipment"])
app.include_router(usage.router, prefix="/api/usage", tags=["Usage"])
