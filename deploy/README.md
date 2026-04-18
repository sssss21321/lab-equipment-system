# 部署指南

## 方案一：Docker 一键部署（推荐，最简单）

### 前提
- 服务器已安装 Docker + Docker Compose
- 如果没有，运行：
  ```bash
  curl -fsSL https://get.docker.com | sh
  apt install -y docker-compose
  ```

### 部署步骤

**第一步：上传代码到服务器**

将整个项目上传到服务器（可以用 scp、rsync 或 Git）：
```bash
# 方式A：Git 克隆（推荐先把代码上传到 GitHub/Gitee）
git clone https://你的仓库地址
cd lab-equipment-system/deploy

# 方式B：scp 上传（本地执行）
scp -r C:/Users/HP/.qclaw/workspace/lab-equipment-system root@你的服务器IP:/root/
```

**第二步：一键启动**
```bash
cd /root/lab-equipment-system/deploy
docker-compose up -d
```

**第三步：访问**
```
http://你的服务器IP
```

---

## 方案二：传统部署（Nginx + systemd）

### 前提
- Ubuntu 22.04 服务器
- SSH 登录到服务器

### 部署步骤

**第一步：上传代码**
```bash
scp -r C:/Users/HP/.qclaw/workspace/lab-equipment-system root@你的服务器IP:/opt/
```

**第二步：运行部署脚本**
```bash
ssh root@你的服务器IP
cd /opt/lab-equipment-system/deploy
bash deploy.sh
```

---

## 方案三：购买云服务器后完整步骤

### Step 1：购买服务器
推荐（任选其一）：
- 腾讯云轻量应用服务器：https://cloud.tencent.com/product/lighthouse（约 30元/月）
- 阿里云 ECS：https://www.aliyun.com（约 50元/月）
- Vultr：https://www.vultr.com（$6/月起）

配置推荐：Ubuntu 22.04，2核4G，50G硬盘

### Step 2：域名（可选）
- 万网/腾讯云购买域名（如 `lab.xxx.com`）
- 域名解析到服务器 IP
- 如果没有域名，直接用 IP 访问即可

### Step 3：本地打包代码
```bash
cd C:\Users\HP\.qclaw\workspace\lab-equipment-system
# 已完成！前端 dist/ 和后端代码都在项目里
```

### Step 4：上传并部署（见上方方案一或二）

### Step 5：设置防火墙
在云服务器控制台开放：
- 端口 80（HTTP）
- 端口 443（HTTPS，可选）
- 端口 22（SSH）

---

## 常见问题

**Q：数据库存在哪里？**
A：SQLite 数据库文件在 `backend/app.db`。Docker 部署时已配置数据持久化到 `data/` 目录，不会因容器重启丢失。

**Q：如何备份数据？**
A：定期备份 `backend/app.db` 文件即可。Docker 环境：`docker cp lab-equipment-system:/app/backend/data/app.db ./backup.db`

**Q：如何更新部署？**
A：
```bash
# Docker 方式
docker-compose down
git pull
docker-compose up -d --build

# 传统方式
bash deploy.sh
```

**Q：如何绑定域名+开启 HTTPS？**
A：部署完成后，运行：
```bash
certbot --nginx -d your-domain.com
```

**Q：如何限制只能特定 IP 访问？**
A：在 Nginx 配置中添加 IP 白名单：
```nginx
allow 192.168.1.0/24;   # 允许的 IP 段
allow 10.0.0.0/8;
deny all;                # 拒绝其他所有
```
