# ============================================================
# 实验室设备管理系统 - 多阶段构建
# ============================================================

# 阶段1：构建前端
FROM node:20-alpine AS frontend

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# 阶段2：运行服务
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./app/
COPY entrypoint.py .

COPY --from=frontend /app/dist ./dist/

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["python", "entrypoint.py"]
