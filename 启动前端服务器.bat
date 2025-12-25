@echo off
chcp 65001 >nul
title PDF表格提取工具 - 前端服务器

echo ========================================
echo PDF表格提取工具 - 前端开发服务器
echo ========================================
echo.
echo 注意：此项目使用Flask后端提供前端服务
echo 推荐方式：访问 http://localhost:5000
echo.
echo 如果需要独立前端服务器（仅用于开发调试），
echo 可以使用Python的简单HTTP服务器
echo.
echo ========================================
echo.

cd /d "%~dp0frontend"

echo 正在启动前端开发服务器...
echo 前端地址: http://localhost:8000
echo.
echo 注意：独立前端服务器无法访问后端API
echo 请确保后端服务器在 http://localhost:5000 运行
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python -m http.server 8000

pause

