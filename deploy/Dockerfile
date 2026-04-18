# ============================================================
# 实验室设备管理系统 - Dockerfile
# 一键部署到任意 Linux 服务器
# ============================================================
# 构建方法：
#   docker build -t lab-system .
#   docker run -d --name lab-system -p 8000:8000 lab-system
# ============================================================

FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/ ./frontend/
WORKDIR /app/frontend

# 前端构建时修正 API 地址为 /api（相对路径，走 Nginx 代理）
# 如果需要指定后端地址，取消下行注释并填入实际地址
# RUN sed -i "s|'/api/|'/api|g" src/api/equipment.js src/api/usage.js

RUN npm install && npm run build

# ============================================================

FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY backend/ ./backend/
COPY requirements.txt ./

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制前端构建产物
COPY --from=frontend-builder /app/frontend/dist /var/www/html

# 配置 Nginx（前后端合一）
RUN echo '' > /etc/nginx/sites-available/default
RUN cat > /etc/nginx/sites-available/default << 'NGINX_EOF'
server {
    listen 80 default_server;
    server_name _;

    root /var/www/html;
    index index.html;

    # 前端路由（支持 SPA）
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态资源缓存
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
NGINX_EOF

RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default \
    && rm -f /etc/nginx/nginx.conf \
    && cat > /etc/nginx/nginx.conf << 'NGINX_CONF'
user root;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events { worker_connections 1024; }

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log /var/log/nginx/access.log;
    sendfile on;
    keepalive_timeout 65;
    include /etc/nginx/sites-enabled/*;
}
NGINX_CONF

# 启动脚本
RUN echo '' > /start.sh
RUN cat > /start.sh << 'START_EOF'
#!/bin/bash

# 启动 Nginx（前台）
nginx &

# 启动后端
cd /app/backend
export PYTHONPATH=/app/backend
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
START_EOF

RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
