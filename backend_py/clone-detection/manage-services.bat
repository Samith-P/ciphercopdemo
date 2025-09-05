@echo off
setlocal enabledelayedexpansion

:menu
cls
echo ================================
echo  Clone Detection Service Manager
echo ================================
echo.
echo 1. Start Both Services (AI + ML)
echo 2. Stop Both Services
echo 3. Check Service Status
echo 4. Start AI Service Only (Port 5003)
echo 5. Start ML Service Only (Port 5000)
echo 6. Exit
echo.
set /p choice="Select an option (1-6): "

if "%choice%"=="1" goto start_both
if "%choice%"=="2" goto stop_both
if "%choice%"=="3" goto check_status
if "%choice%"=="4" goto start_ai
if "%choice%"=="5" goto start_ml
if "%choice%"=="6" goto exit
goto menu

:start_both
echo.
echo Starting AI Service (Port 5003)...
start "AI Service - Gemini" cmd /c "cd /d %~dp0gemini && call .venv\Scripts\activate && python app.py"
timeout /t 2 >nul

echo Starting ML Service (Port 5000)...
start "ML Service - Phishpedia" cmd /c "cd /d %~dp0phishpedia+detectron2\Phishpedia && call phishpedia_env\Scripts\activate && cd WEBtool && python app.py"

echo.
echo Both services are starting...
echo Wait 10-15 seconds for services to be ready.
echo.
pause
goto menu

:start_ai
echo.
echo Starting AI Service (Port 5003)...
start "AI Service - Gemini" cmd /c "cd /d %~dp0gemini && call .venv\Scripts\activate && python app.py"
echo AI Service started.
pause
goto menu

:start_ml
echo.
echo Starting ML Service (Port 5000)...
start "ML Service - Phishpedia" cmd /c "cd /d %~dp0phishpedia+detectron2\Phishpedia && call phishpedia_env\Scripts\activate && cd WEBtool && python app.py"
echo ML Service started.
pause
goto menu

:stop_both
echo.
echo Stopping services by window title...

REM Kill AI Service
taskkill /FI "WINDOWTITLE eq AI Service - Gemini*" /F >nul 2>&1
if %errorlevel%==0 (
    echo Stopped AI Service (Port 5003).
) else (
    echo AI Service not running.
)

REM Kill ML Service
taskkill /FI "WINDOWTITLE eq ML Service - Phishpedia*" /F >nul 2>&1
if %errorlevel%==0 (
    echo Stopped ML Service (Port 5000).
) else (
    echo ML Service not running.
)

echo.
pause
goto menu

:check_status
echo.
echo Checking service status...
echo.

REM Check port 5000
netstat -an | findstr ":5000" | findstr "LISTENING" >nul
if %errorlevel%==0 (
    echo ✅ ML Service (Port 5000): RUNNING
) else (
    echo ❌ ML Service (Port 5000): NOT RUNNING
)

REM Check port 5003
netstat -an | findstr ":5003" | findstr "LISTENING" >nul
if %errorlevel%==0 (
    echo ✅ AI Service (Port 5003): RUNNING
) else (
    echo ❌ AI Service (Port 5003): NOT RUNNING
)

echo.
pause
goto menu

:exit
echo.
echo Stopping services before exit...

call :stop_both_silent

echo Exiting...
exit /b 0
:stop_both_silent
REM Silent stop (no pause, no menu return)
taskkill /FI "WINDOWTITLE eq AI Service - Gemini*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq ML Service - Phishpedia*" /F >nul 2>&1
exit /b 0
