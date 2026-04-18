#!/bin/bash
# ============================================================
# 实验室设备管理系统 - 一键部署脚本（Ubuntu 22.04）
# ============================================================
# 用法：
#   curl -fsSL https://你的服务器IP/deploy.sh | bash
#   或直接在服务器上运行：
#   bash deploy.sh
# ============================================================

set -e

APP_DIR="/opt/lab-equipment-system"
SERVICE_NAME="lab-backend"
DOMAIN="${DOMAIN:-}"          # 可选：填入域名如 lab.example.com
EMAIL="${EMAIL:-admin@example.com}"  # Let's Encrypt 通知用
GIT_REPO="${GIT_REPO:-}"      # 可选：填入 Git 仓库地址

# 颜色
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo "=========================================="
echo "  实验室设备管理系统 - 部署脚本"
echo "=========================================="

# ---------- 1. 检测操作系统 ----------
if ! grep -q "Ubuntu\|Debian" /etc/os-release 2>/dev/null; then
    error "仅支持 Ubuntu/Debian 系统"
fi
info "系统检查通过 ✓"

# ---------- 2. 更新系统 ----------
info "更新系统软件包..."
apt update && apt upgrade -y

# ---------- 3. 安装依赖 ----------
info "安装依赖：Python3, Node.js, Nginx, Certbot..."
apt install -y \
    python3 python3-pip python3-venv \
    nodejs npm \
    nginx certbot python3-certbot-nginx \
    curl git wget

# ---------- 4. 创建应用目录 ----------
info "创建应用目录..."
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# ---------- 5. 部署后端 ----------
info "部署后端..."

# 如果有 Git 仓库则克隆，否则提示手动上传
if [ -n "$GIT_REPO" ]; then
    git clone "$GIT_REPO" "$APP_DIR/backend" 2>/dev/null || git clone "$GIT_REPO" .
fi

# 创建 Python 虚拟环境
python3 -m venv "$APP_DIR/venv"

# 安装 Python 依赖
if [ -f "$APP_DIR/backend/requirements.txt" ]; then
    "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"
elif [ -f "requirements.txt" ]; then
    "$APP_DIR/venv/bin/pip" install -r requirements.txt
else
    "$APP_DIR/venv/bin/pip" install fastapi uvicorn[standard] sqlalchemy aiosqlite python-multipart pydantic
fi

# 创建 systemd 服务文件
info "配置 systemd 服务..."
cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=Lab Equipment System Backend
After=network.target

[Service]
WorkingDirectory=${APP_DIR}/backend
ExecStart=${APP_DIR}/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5
Environment="PYTHONPATH=${APP_DIR}/backend"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl restart ${SERVICE_NAME}

# 等待服务启动
sleep 3
if systemctl is-active --quiet ${SERVICE_NAME}; then
    info "后端服务启动成功 ✓"
else
    error "后端服务启动失败，请检查日志：journalctl -u ${SERVICE_NAME} -n 50"
fi

# ---------- 6. 构建前端 ----------
info "构建前端..."

FRONTEND_DIR="$APP_DIR/frontend"
mkdir -p "$FRONTEND_DIR"

# 如果有前端源码则构建（用户需要先把前端代码放到 frontend/ 目录）
if [ -d "$FRONTEND_DIR/src" ]; then
    cd "$FRONTEND_DIR"
    npm install
    npm run build
    info "前端构建完成 ✓"
else
    warn "未找到前端源码，跳过前端构建"
    warn "请将前端代码放入：$FRONTEND_DIR"
    warn "然后运行：cd $FRONTEND_DIR && npm install && npm run build"
fi

# ---------- 7. 配置 Nginx ----------
info "配置 Nginx..."

NGINX_CONF="/etc/nginx/sites-available/lab-system"
NGINX_ENABLED="/etc/nginx/sites-enabled/lab-system"

cat > "$NGINX_CONF" << 'EOF'
server {
    listen 80;
    server_name _;

    root /opt/lab-equipment-system/frontend/dist;
    index index.html;

    # 前端静态文件
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 反向代理
    location /api/ {
        proxy_pass http://127.00.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 前端开发代理（备选）
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用站点
ln -sf "$NGINX_CONF" "$NGINX_ENABLED"
# 移除默认站点（如果有冲突）
rm -f /etc/nginx/sites-enabled/default

# 测试配置
nginx -t || error "Nginx 配置有误"
systemctl reload nginx
systemctl enable nginx

info "Nginx 启动成功 ✓"

# ---------- 8. HTTPS（可选） ----------
if [ -n "$DOMAIN" ]; then
    info "配置 HTTPS（Let's Encrypt）..."
    certbot --nginx -d "$DOMAIN" --noninteractive --agree-tos -m "$EMAIL"
    info "HTTPS 配置完成 ✓"
    info "访问地址：https://$DOMAIN"
else
    SERVER_IP=$(curl -s ifconfig.me || echo "你的服务器IP")
    info "部署完成！访问地址：http://$SERVER_IP"
fi

# ---------- 9. 完成 ----------
echo ""
echo "=========================================="
echo -e "  ${GREEN}部署完成！${NC}"
echo "=========================================="
echo ""
echo "服务状态："
systemctl status ${SERVICE_NAME} --no-pager | head -5
echo ""
echo "常用命令："
echo "  重启后端：  systemctl restart ${SERVICE_NAME}"
echo "  查看日志：  journalctl -u ${SERVICE_NAME} -f"
echo "  重启Nginx： systemctl reload nginx"
echo "  更新部署：  bash $APP_DIR/deploy.sh"
echo ""
echo "前端目录：$FRONTEND_DIR"
echo "后端目录：$APP_DIR/backend"
echo "数据库：  $APP_DIR/backend/app.db"
echo ""
