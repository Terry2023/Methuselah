@echo off
title METHUSELAH LAUNCH CONTROL
color 0A

echo ========================================
echo  METHUSELAH SOVEREIGN DASHBOARD STARTUP
echo ========================================
echo.

:: 1. Kill any old processes so we start clean
echo [1/4] Terminating old processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM ollama.exe >nul 2>&1
timeout /t 1 >nul

:: 2. Start Ollama in background
echo [2/4] Starting Ollama serve...
start "Ollama" /MIN cmd /c "ollama serve"
echo       Waiting 5 seconds for CUDA init...
timeout /t 5 >nul

:: 3. Start Python Bridge in background  
echo [3/4] Starting 7950x Brain bridge...
cd /d D:\project\dashboard\src
start "Brain" /MIN cmd /c "python main.py"
echo       Waiting 3 seconds for FastAPI...
timeout /t 3 >nul

:: 4. Start HTTP Server in background
echo [4/4] Starting Dashboard HTTP server...
cd /d D:\project\dashboard
start "HTTP" /MIN cmd /c "python -m http.server 8080"
echo       Waiting 2 seconds for server...
timeout /t 2 >nul

:: 5. Open browser automatically
echo.
echo All systems online. Opening dashboard...
start http://localhost:8080

echo.
echo ========================================
echo  METHUSELAH IS LIVE
echo  Ollama ^| Brain ^| HTTP running in background
echo  Close this window to stop all services
echo ========================================
echo.

:: Keep window open and wait for user to close
pause >nul

:: Cleanup when you close this window
echo Shutting down METHUSELAH...
taskkill /F /FI "WindowTitle eq Ollama*" >nul 2>&1
taskkill /F /FI "WindowTitle eq Brain*" >nul 2>&1  
taskkill /F /FI "WindowTitle eq HTTP*" >nul 2>&1