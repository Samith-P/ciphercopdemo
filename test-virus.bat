@echo off
setlocal

echo ===========================
echo  Testing Malware-Virus (5004)
echo ===========================
echo.

:: Go to the Virus service folder
cd /d "D:\volume E\ciphercop-2025\overall\ciphercopdemo\backend_py\malware-detection\ml-detection\Virus_total_based"

:: Check if app.py exists
if not exist app.py (
    echo ❌ ERROR: app.py not found in %cd%
    pause
    exit /b 1
)

:: Check if the venv Python exists
if not exist "D:\volume E\ciphercop-2025\overall\ciphercopdemo\backend_py\malware-detection\ml-detection\.venv\Scripts\python.exe" (
    echo ❌ ERROR: Python executable not found at .venv\Scripts\python.exe
    pause
    exit /b 1
)

:: Print Python version for confirmation
echo ✅ Found Python. Version is:
"D:\volume E\ciphercop-2025\overall\ciphercopdemo\backend_py\malware-detection\ml-detection\.venv\Scripts\python.exe" --version
echo.

:: Run app.py with correct path
echo Running app.py now...
"D:\volume E\ciphercop-2025\overall\ciphercopdemo\backend_py\malware-detection\ml-detection\.venv\Scripts\python.exe" "D:\volume E\ciphercop-2025\overall\ciphercopdemo\backend_py\malware-detection\ml-detection\Virus_total_based\app.py"

echo.
echo [*] Malware-Virus test finished.
pause
