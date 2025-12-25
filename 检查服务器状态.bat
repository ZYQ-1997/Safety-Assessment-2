@echo off
chcp 65001 >nul
title 检查服务器状态

echo ========================================
echo PDF表格提取工具 - 服务器状态检查
echo ========================================
echo.

echo [1] 检查端口5000是否被占用...
netstat -ano | findstr :5000 >nul
if %errorlevel% == 0 (
    echo ✓ 端口5000已被占用（服务器可能正在运行）
    netstat -ano | findstr :5000
) else (
    echo ✗ 端口5000未被占用（服务器未运行）
)
echo.

echo [2] 检查Python进程...
tasklist | findstr python.exe >nul
if %errorlevel% == 0 (
    echo ✓ 发现Python进程
    tasklist | findstr python.exe
) else (
    echo ✗ 未发现Python进程
)
echo.

echo [3] 测试服务器响应...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000' -UseBasicParsing -TimeoutSec 3; Write-Host '✓ 服务器响应成功！状态码:' $response.StatusCode } catch { Write-Host '✗ 服务器未响应:' $_.Exception.Message }"
echo.

echo [4] 测试API接口...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -UseBasicParsing -TimeoutSec 3; Write-Host '✓ API接口正常！状态码:' $response.StatusCode } catch { Write-Host '✗ API接口无响应:' $_.Exception.Message }"
echo.

echo ========================================
echo 访问地址:
echo   前端页面: http://localhost:5000
echo   API接口: http://localhost:5000/api
echo ========================================
echo.

echo 如果服务器未运行，请运行"启动服务器.bat"
echo.

pause

