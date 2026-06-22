# AI Agent 情报站 — 一键启动
# 用法：在 PowerShell 中运行 .\product\start.ps1

$ROOT    = Split-Path -Parent $PSScriptRoot
$PRODUCT = $PSScriptRoot
$API     = Join-Path $PRODUCT "api"
$PYTHON  = "python"

Write-Host ""
Write-Host "=== AI Agent 情报站 ===" -ForegroundColor Cyan

# 1. 检查依赖
Write-Host "[1] 检查 Python 依赖..." -ForegroundColor Yellow
& $PYTHON -c "import flask, openai, feedparser, supermemo2" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    缺少依赖，正在安装..." -ForegroundColor Yellow
    & $PYTHON -m pip install -r "$PRODUCT\requirements.txt" -q
}

# 2. 初始化数据库（幂等）
Write-Host "[2] 初始化数据库..." -ForegroundColor Yellow
& $PYTHON "$PRODUCT\scripts\migrate_db.py" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    数据库初始化失败，请检查 product/scripts/migrate_db.py" -ForegroundColor Red
    exit 1
}

# 3. 启动 Flask
$HOST = "127.0.0.1"
$PORT = "5000"
Write-Host "[3] 启动服务 http://${HOST}:${PORT}" -ForegroundColor Green
Write-Host ""
Write-Host "    主界面:   http://${HOST}:${PORT}/" -ForegroundColor White
Write-Host "    知识图谱: http://${HOST}:${PORT}/graph" -ForegroundColor White
Write-Host "    API 文档: http://${HOST}:${PORT}/api/health" -ForegroundColor White
Write-Host ""
Write-Host "    按 Ctrl+C 停止服务" -ForegroundColor Gray
Write-Host ""

# 自动打开浏览器（3秒后）
Start-Job -ScriptBlock {
    Start-Sleep 3
    Start-Process "http://127.0.0.1:5000/"
} | Out-Null

# 启动 Flask（前台运行）
Set-Location $API
& $PYTHON "app.py"
