#!/bin/bash
# 快速部署脚本

echo "=========================================="
echo "PDF表格提取工具 - 部署脚本"
echo "=========================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: 未找到Docker，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: 未找到docker-compose，请先安装docker-compose"
    exit 1
fi

echo "1. 停止现有容器..."
docker-compose down

echo "2. 构建Docker镜像..."
docker-compose build

echo "3. 启动服务..."
docker-compose up -d

echo "4. 等待服务启动..."
sleep 5

echo "5. 检查服务状态..."
docker-compose ps

echo "6. 查看日志..."
echo "使用以下命令查看日志: docker-compose logs -f"
echo "使用以下命令停止服务: docker-compose down"

echo ""
echo "=========================================="
echo "部署完成！"
echo "服务地址: http://localhost:5000"
echo "=========================================="

