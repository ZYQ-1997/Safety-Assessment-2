@echo off
chcp 65001 >nul
title 提交代码到GitHub

echo ==========================================
echo 提交代码到GitHub
echo ==========================================
echo.

REM 检查Git是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Git
    echo.
    echo 请先安装Git:
    echo 1. 下载: https://git-scm.com/download/win
    echo 2. 或使用GitHub Desktop: https://desktop.github.com
    echo.
    pause
    exit /b 1
)

echo [1/4] 检查Git状态...
git status

echo.
echo [2/4] 添加所有文件...
git add .

echo.
echo [3/4] 提交更改...
set /p commit_msg="请输入提交信息 (直接回车使用默认): "
if "%commit_msg%"=="" set commit_msg=Update: Fix API URL for production deployment

git commit -m "%commit_msg%"

echo.
echo [4/4] 推送到GitHub...
echo.
echo 提示: 如果提示输入用户名和密码，请使用GitHub的Personal Access Token
echo 生成Token: https://github.com/settings/tokens
echo.

REM 检查远程仓库
git remote -v >nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置远程仓库
    echo.
    set /p repo_url="请输入GitHub仓库URL (例如: https://github.com/用户名/仓库名.git): "
    if not "%repo_url%"=="" (
        git remote add origin "%repo_url%"
    ) else (
        echo 未设置远程仓库，跳过推送
        pause
        exit /b 0
    )
)

git push origin main
if errorlevel 1 (
    echo.
    echo [错误] 推送失败
    echo.
    echo 可能的原因:
    echo 1. 远程仓库地址错误
    echo 2. 需要配置SSH密钥或使用HTTPS
    echo.
    echo 解决方案:
    echo 1. 使用GitHub Desktop推送（推荐）
    echo 2. 或运行: 快速修复推送.bat
    echo.
) else (
    echo.
    echo ==========================================
    echo ✅ 代码已成功推送到GitHub！
    echo ==========================================
    echo.
    echo Railway会自动检测并重新部署
    echo 请等待2-5分钟...
    echo.
)

pause

