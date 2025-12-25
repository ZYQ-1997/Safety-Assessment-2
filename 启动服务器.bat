@echo off
chcp 65001 >nul
title PDF表格提取工具 - 后端服务器

echo ========================================
echo PDF表格提取工具 - 后端服务器
echo ========================================
echo.

cd /d "%~dp0"

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo.
echo 正在启动后端服务器...
echo.
echo ========================================
echo 前端界面: http://localhost:5000
echo API接口: http://localhost:5000/api
echo ========================================
echo.
echo 请在浏览器中访问: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

cd backend
python app.py

if errorlevel 1 (
    echo.
    echo [错误] 服务器启动失败
    echo 请检查错误信息 above
    pause
)

