@echo off
chcp 65001 >nul
title PDF表格提取工具 - 快速部署向导

echo ==========================================
echo PDF表格提取工具 - 快速部署向导
echo ==========================================
echo.
echo 请选择部署方式:
echo.
echo [1] 部署到Railway（推荐，免费，自动）
echo [2] 部署到本地Docker
echo [3] 部署到云服务器
echo.
set /p choice="请输入选项 (1-3): "

if "%choice%"=="1" goto railway
if "%choice%"=="2" goto local
if "%choice%"=="3" goto server
goto end

:railway
echo.
echo ==========================================
echo 部署到Railway
echo ==========================================
echo.
echo 步骤1: 确保代码已推送到GitHub
echo 步骤2: 访问 https://railway.app
echo 步骤3: 使用GitHub登录
echo 步骤4: 点击 "New Project" → "Deploy from GitHub repo"
echo 步骤5: 选择您的仓库
echo.
echo Railway会自动部署您的应用！
echo.
echo 详细说明请查看: setup_railway.md
echo.
pause
goto end

:local
echo.
echo ==========================================
echo 部署到本地Docker
echo ==========================================
echo.
call deploy.bat
goto end

:server
echo.
echo ==========================================
echo 部署到云服务器
echo ==========================================
echo.
echo 请输入服务器信息:
set /p server_host="服务器IP或域名: "
set /p server_user="SSH用户名 (默认: root): "
if "%server_user%"=="" set server_user=root
set /p server_key="SSH密钥路径 (可选，直接回车跳过): "

echo.
echo 开始部署到 %server_user%@%server_host%...
python auto_deploy.py server
goto end

:end
echo.
echo 部署完成！
pause

