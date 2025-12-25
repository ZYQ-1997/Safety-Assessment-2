@echo off
chcp 65001 >nul
title 一键提交代码到GitHub

echo ==========================================
echo 一键提交代码到GitHub
echo ==========================================
echo.

REM 检查Git是否安装
where git >nul 2>&1
if errorlevel 1 (
    echo [提示] 未检测到Git命令行工具
    echo.
    echo 推荐使用GitHub Desktop（更简单）:
    echo 1. 下载: https://desktop.github.com
    echo 2. 打开GitHub Desktop
    echo 3. File → Add Local Repository
    echo 4. 选择项目文件夹
    echo 5. 点击 "Commit to main" → "Push origin"
    echo.
    echo 正在打开GitHub Desktop下载页面...
    start https://desktop.github.com
    echo.
    pause
    exit /b 0
)

echo [1/5] 检查Git状态...
git status
echo.

echo [2/5] 添加所有更改的文件...
git add .
if errorlevel 1 (
    echo [错误] 添加文件失败
    pause
    exit /b 1
)
echo ✅ 文件已添加

echo.
echo [3/5] 提交更改...
git commit -m "Fix API URL for production deployment and improve CORS configuration"
if errorlevel 1 (
    echo [警告] 提交失败，可能没有更改需要提交
    echo 继续尝试推送...
) else (
    echo ✅ 更改已提交
)

echo.
echo [4/5] 检查远程仓库...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置远程仓库
    echo.
    set /p repo_url="请输入GitHub仓库URL: "
    if not "!repo_url!"=="" (
        git remote add origin "!repo_url!"
        echo ✅ 远程仓库已添加
    ) else (
        echo [错误] 未设置远程仓库，无法推送
        echo.
        echo 请运行以下命令设置远程仓库:
        echo   git remote add origin https://github.com/您的用户名/您的仓库名.git
        pause
        exit /b 1
    )
)

echo.
echo [5/5] 推送到GitHub...
echo.
echo 提示: 如果要求输入密码，请使用GitHub的Personal Access Token
echo 生成Token: https://github.com/settings/tokens
echo.

git push origin main
if errorlevel 1 (
    echo.
    echo ==========================================
    echo [错误] 推送失败
    echo ==========================================
    echo.
    echo 可能的原因:
    echo 1. 需要配置SSH密钥
    echo 2. 需要使用Personal Access Token
    echo 3. 远程仓库地址错误
    echo.
    echo 解决方案:
    echo 1. 使用GitHub Desktop推送（推荐）
    echo 2. 运行: 快速修复推送.bat
    echo 3. 查看: 如何提交代码.md
    echo.
) else (
    echo.
    echo ==========================================
    echo ✅ 代码已成功推送到GitHub！
    echo ==========================================
    echo.
    echo Railway会自动检测并重新部署
    echo 请等待2-5分钟，然后测试您的应用
    echo.
)

pause

