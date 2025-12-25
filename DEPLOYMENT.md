# 部署指南

本文档介绍如何将PDF表格提取工具部署到生产环境。

## 部署方式

### 方式1: 使用Docker（推荐）

#### 1. 构建Docker镜像

```bash
docker build -t pdf-table-extractor .
```

#### 2. 运行容器

```bash
docker run -d \
  --name pdf-extractor \
  -p 5000:5000 \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  -v $(pwd)/backend/outputs:/app/backend/outputs \
  -v $(pwd)/logs:/app/logs \
  pdf-table-extractor
```

#### 3. 使用Docker Compose（推荐）

```bash
docker-compose up -d
```

查看日志：
```bash
docker-compose logs -f
```

停止服务：
```bash
docker-compose down
```

### 方式2: 使用Gunicorn（Linux/Unix）

#### 1. 安装依赖

```bash
pip install -r requirements.txt
pip install gunicorn
```

#### 2. 创建日志目录

```bash
mkdir -p logs
```

#### 3. 启动服务

```bash
cd backend
gunicorn --config ../gunicorn_config.py wsgi:app
```

#### 4. 使用systemd管理服务（可选）

创建服务文件 `/etc/systemd/system/pdf-extractor.service`:

```ini
[Unit]
Description=PDF Table Extractor
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Safety Assessment/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn --config /path/to/gunicorn_config.py wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl start pdf-extractor
sudo systemctl enable pdf-extractor
```

### 方式3: 使用云平台部署

#### Railway

1. 在Railway上创建新项目
2. 连接GitHub仓库
3. Railway会自动检测Dockerfile并部署
4. 设置环境变量（如需要）

#### Render

1. 在Render上创建新的Web Service
2. 连接GitHub仓库
3. 设置构建命令：`docker build -t app .`
4. 设置启动命令：`docker run -p 5000:5000 app`
5. 设置环境变量

#### Heroku

1. 创建 `Procfile`:
```
web: gunicorn --config gunicorn_config.py wsgi:app
```

2. 部署：
```bash
heroku create your-app-name
git push heroku main
```

#### 阿里云/腾讯云/华为云

1. 购买云服务器（建议2核4G以上）
2. 安装Docker：
```bash
curl -fsSL https://get.docker.com | bash
```

3. 使用Docker Compose部署：
```bash
docker-compose up -d
```

## 配置Nginx反向代理（推荐）

### 安装Nginx

```bash
sudo apt-get update
sudo apt-get install nginx
```

### 配置Nginx

创建配置文件 `/etc/nginx/sites-available/pdf-extractor`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名

    client_max_body_size 500M;  # 允许上传最大500MB文件

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/pdf-extractor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 配置HTTPS（使用Let's Encrypt）

### 安装Certbot

```bash
sudo apt-get install certbot python3-certbot-nginx
```

### 获取SSL证书

```bash
sudo certbot --nginx -d your-domain.com
```

Certbot会自动配置Nginx使用HTTPS。

## 防火墙配置

```bash
# 允许HTTP和HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 如果直接访问5000端口（不推荐）
sudo ufw allow 5000/tcp
```

## 监控和日志

### 查看应用日志

```bash
# Docker方式
docker-compose logs -f

# Gunicorn方式
tail -f logs/error.log
tail -f logs/access.log
```

### 健康检查

访问 `http://your-domain.com/api/health` 检查服务状态。

## 性能优化

1. **增加工作进程数**：修改 `gunicorn_config.py` 中的 `workers` 参数
2. **使用CDN**：将静态文件托管到CDN
3. **启用缓存**：使用Redis缓存频繁访问的数据
4. **负载均衡**：使用多个实例和负载均衡器

## 安全建议

1. **使用HTTPS**：始终使用HTTPS加密传输
2. **限制文件大小**：已在代码中设置500MB限制
3. **定期清理**：定期清理 `uploads` 和 `outputs` 目录中的旧文件
4. **访问控制**：如需限制访问，可以添加认证机制
5. **更新依赖**：定期更新依赖包以修复安全漏洞

## 备份

定期备份重要数据：

```bash
# 备份上传的文件和输出结果
tar -czf backup-$(date +%Y%m%d).tar.gz backend/uploads backend/outputs
```

## 故障排除

### 服务无法启动

1. 检查端口是否被占用：
```bash
netstat -tulpn | grep 5000
```

2. 检查日志文件：
```bash
tail -f logs/error.log
```

3. 检查Python环境：
```bash
python --version
pip list
```

### 文件上传失败

1. 检查文件大小限制（Nginx和Flask都需要配置）
2. 检查磁盘空间：
```bash
df -h
```

3. 检查目录权限：
```bash
ls -la backend/uploads
```

### 性能问题

1. 增加Gunicorn工作进程数
2. 使用更强大的服务器
3. 优化PDF处理逻辑

## 更新部署

```bash
# Docker方式
docker-compose down
git pull
docker-compose build
docker-compose up -d

# Gunicorn方式
systemctl restart pdf-extractor
```

## 联系支持

如遇到问题，请查看日志文件或联系技术支持。

