@echo off
chcp 65001 >nul
echo ==========================================
echo PDF表格提取工具 - 部署脚本 (Windows)
echo ==========================================
echo.

REM 检查Docker是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Docker，请先安装Docker Desktop
    echo 下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM 检查docker-compose是否安装
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到docker-compose，请先安装docker-compose
    pause
    exit /b 1
)

echo [1/5] 停止现有容器...
docker-compose down

echo.
echo [2/5] 构建Docker镜像...
docker-compose build

echo.
echo [3/5] 启动服务...
docker-compose up -d

echo.
echo [4/5] 等待服务启动...
timeout /t 5 /nobreak >nul

echo.
echo [5/5] 检查服务状态...
docker-compose ps

echo.
echo ==========================================
echo 部署完成！
echo ==========================================
echo 服务地址: http://localhost:5000
echo.
echo 常用命令:
echo   查看日志: docker-compose logs -f
echo   停止服务: docker-compose down
echo   重启服务: docker-compose restart
echo ==========================================
echo.
pause

