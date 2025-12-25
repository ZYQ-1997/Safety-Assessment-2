@echo off
chcp 65001 >nul
title PDF表格提取工具 - 一键部署

echo ==========================================
echo PDF表格提取工具 - 一键部署
echo ==========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Docker，请先安装Docker Desktop
    echo.
    echo 正在打开Docker下载页面...
    start https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/3] 检查环境...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [警告] Docker未运行，请启动Docker Desktop
    pause
    exit /b 1
)

echo [2/3] 开始部署...
python auto_deploy.py local

echo.
echo [3/3] 部署完成！
echo.
echo 访问地址: http://localhost:5000
echo.
echo 按任意键退出...
pause >nul

