@echo off
cd /d C:\Users\HP\.qclaw\workspace\lab-equipment-system\backend
C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
