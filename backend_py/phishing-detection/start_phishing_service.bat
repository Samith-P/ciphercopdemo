@echo off
echo Starting ML-Based Phishing Detection Service...
echo.

cd /d "C:\CC2025\ciphercopdemo\backend_py\phishing-detection"

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Starting Flask application on port 5003...
python app.py

pause
