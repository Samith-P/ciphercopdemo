@echo off
echo ========================================
echo   Email & SMS Notification System Setup
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [2/4] Installing required packages...
pip install -r requirements.txt

echo [3/4] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo .env file created from .env.example
    echo Please edit .env file with your credentials before running the app
) else (
    echo .env file already exists
)

echo [4/4] Setup completed!
echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo 1. Edit .env file with your credentials:
echo    - Gmail email and app password
echo    - Twilio account details
echo    - Redis URL (optional)
echo.
echo 2. Run the application:
echo    python app.py
echo.
echo 3. Open your browser:
echo    http://localhost:5000
echo ========================================
echo.
pause
