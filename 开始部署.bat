@echo off
chcp 65001 >nul
title PDF表格提取工具 - 开始部署

echo ==========================================
echo PDF表格提取工具 - 开始部署
echo ==========================================
echo.
echo 您没有云服务器，我们使用免费的云平台部署！
echo.
echo 推荐方案：Railway（完全免费，自动部署）
echo.
echo ==========================================
echo 第一步：准备GitHub仓库
echo ==========================================
echo.
echo 请选择：
echo [1] 我已经有GitHub仓库
echo [2] 我需要创建GitHub仓库（推荐）
echo [3] 我想使用Railway CLI直接部署
echo.
set /p step1="请选择 (1-3): "

if "%step1%"=="1" goto deploy
if "%step1%"=="2" goto create_repo
if "%step1%"=="3" goto railway_cli
goto end

:create_repo
echo.
echo ==========================================
echo 创建GitHub仓库
echo ==========================================
echo.
echo 方法1: 使用GitHub Desktop（最简单）
echo ------------------------------------------
echo 1. 下载GitHub Desktop: https://desktop.github.com
echo 2. 安装并登录
echo 3. 点击 "File" → "Add Local Repository"
echo 4. 选择当前文件夹
echo 5. 点击 "Publish repository"
echo.
echo 方法2: 使用网页
echo ------------------------------------------
echo 1. 访问: https://github.com/new
echo 2. 创建新仓库
echo 3. 上传项目文件
echo.
echo 创建完成后，按任意键继续...
pause >nul
goto deploy

:railway_cli
echo.
echo ==========================================
echo 使用Railway CLI部署
echo ==========================================
echo.
echo 1. 安装Railway CLI:
echo    npm install -g @railway/cli
echo.
echo 2. 登录:
echo    railway login
echo.
echo 3. 部署:
echo    railway init
echo    railway up
echo.
echo 详细说明请查看: 最简单部署指南.md
pause
goto end

:deploy
echo.
echo ==========================================
echo 部署到Railway
echo ==========================================
echo.
echo 步骤：
echo 1. 访问: https://railway.app
echo 2. 点击 "Login" → 选择 "Login with GitHub"
echo 3. 点击 "New Project"
echo 4. 选择 "Deploy from GitHub repo"
echo 5. 选择您的仓库
echo 6. Railway会自动部署！
echo.
echo 正在打开Railway网站...
start https://railway.app
echo.
echo 详细说明请查看: 最简单部署指南.md
echo.
pause
goto end

:end
echo.
echo ==========================================
echo 完成！
echo ==========================================
echo.
echo 如果遇到问题，请查看: 最简单部署指南.md
echo.
pause

