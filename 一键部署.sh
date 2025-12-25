#!/bin/bash
# 一键部署脚本

set -e

echo "=========================================="
echo "PDF表格提取工具 - 一键部署"
echo "=========================================="
echo

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未找到Docker，请先安装Docker"
    echo "安装命令: curl -fsSL https://get.docker.com | bash"
    exit 1
fi

# 检查Docker是否运行
if ! docker ps &> /dev/null; then
    echo "❌ Docker未运行，请启动Docker服务"
    echo "启动命令: sudo systemctl start docker"
    exit 1
fi

echo "✅ 环境检查通过"
echo
echo "🚀 开始部署..."
echo

python3 auto_deploy.py local

echo
echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
echo "访问地址: http://localhost:5000"
echo

