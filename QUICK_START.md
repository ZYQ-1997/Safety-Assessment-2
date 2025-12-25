# 快速部署指南

## 🚀 最简单的方式：使用Docker（推荐）

### Windows用户

1. **安装Docker Desktop**
   - 下载：https://www.docker.com/products/docker-desktop
   - 安装并启动Docker Desktop

2. **运行部署脚本**
   ```bash
   deploy.bat
   ```

3. **访问服务**
   - 打开浏览器访问：http://localhost:5000

### Linux/Mac用户

1. **安装Docker和Docker Compose**
   ```bash
   # Linux
   curl -fsSL https://get.docker.com | bash
   sudo apt-get install docker-compose
   
   # Mac (使用Homebrew)
   brew install docker docker-compose
   ```

2. **运行部署脚本**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **访问服务**
   - 打开浏览器访问：http://localhost:5000

## 🌐 部署到云服务器

### 步骤1: 准备云服务器

推荐配置：
- **CPU**: 2核以上
- **内存**: 4GB以上
- **系统**: Ubuntu 20.04/22.04 或 CentOS 7/8
- **磁盘**: 50GB以上（用于存储上传的文件）

### 步骤2: 连接到服务器

```bash
ssh username@your-server-ip
```

### 步骤3: 安装Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER

# CentOS/RHEL
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### 步骤4: 上传项目文件

```bash
# 在本地使用scp上传（或使用Git）
scp -r "Safety Assessment" username@your-server-ip:/opt/
```

### 步骤5: 在服务器上部署

```bash
cd /opt/Safety\ Assessment
docker-compose up -d
```

### 步骤6: 配置防火墙

```bash
# Ubuntu
sudo ufw allow 5000/tcp
sudo ufw reload

# CentOS
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

### 步骤7: 配置域名和HTTPS（可选但推荐）

#### 安装Nginx

```bash
sudo apt-get update
sudo apt-get install nginx
```

#### 配置Nginx反向代理

创建文件 `/etc/nginx/sites-available/pdf-extractor`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名

    client_max_body_size 500M;

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

#### 配置HTTPS（使用Let's Encrypt）

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 📋 常用命令

### Docker Compose命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 查看状态
docker-compose ps

# 重新构建
docker-compose build --no-cache
```

### 查看服务状态

```bash
# 检查服务是否运行
curl http://localhost:5000/api/health

# 查看容器日志
docker-compose logs web

# 查看系统资源使用
docker stats
```

## 🔧 故障排除

### 问题1: 端口被占用

```bash
# 检查端口占用
netstat -tulpn | grep 5000

# 修改docker-compose.yml中的端口映射
# 例如改为 8080:5000
```

### 问题2: 文件上传失败

1. 检查磁盘空间：
```bash
df -h
```

2. 检查目录权限：
```bash
ls -la backend/uploads
```

3. 增加Nginx的client_max_body_size（如果使用Nginx）

### 问题3: 服务无法启动

1. 查看详细日志：
```bash
docker-compose logs web
```

2. 检查Docker是否运行：
```bash
docker ps
```

3. 重新构建镜像：
```bash
docker-compose build --no-cache
docker-compose up -d
```

## 🔒 安全建议

1. **使用HTTPS**：始终配置SSL证书
2. **限制访问**：使用防火墙限制访问IP（如需要）
3. **定期更新**：保持Docker和系统更新
4. **备份数据**：定期备份重要文件
5. **监控日志**：定期检查日志文件

## 📞 获取帮助

如果遇到问题：
1. 查看 `DEPLOYMENT.md` 获取详细部署文档
2. 查看日志文件：`docker-compose logs -f`
3. 检查服务健康状态：`curl http://localhost:5000/api/health`

## 🎉 部署成功！

部署完成后，您可以通过以下方式访问服务：
- 本地访问：http://localhost:5000
- 服务器IP访问：http://your-server-ip:5000
- 域名访问：https://your-domain.com（如果配置了域名和HTTPS）

