@echo off
setlocal enabledelayedexpansion

:: ------------------------------------------------------------------------------
:: Phishpedia + Detectron2 Setup Script
:: This script installs PyTorch, Detectron2 (local), and downloads required models
:: ------------------------------------------------------------------------------
echo [%DATE% %TIME%] Starting Phishpedia setup...

:: ------------------------------------------------------------------------------
:: Check if virtual environment exists
:: ------------------------------------------------------------------------------
if not exist "phishpedia_env\Scripts\python.exe" (
    echo [ERROR] Virtual environment 'phishpedia_env' not found!
    echo Please create it first: python -m venv phishpedia_env
    exit /b 1
)

:: ------------------------------------------------------------------------------
:: Tool Checks (Optional - only for model downloads)
:: ------------------------------------------------------------------------------
where gdown >nul 2>nul || (
    echo [WARNING] gdown not found. Installing gdown for model downloads...
    phishpedia_env\Scripts\python.exe -m pip install gdown
)

where unzip >nul 2>nul || (
    echo [ERROR] unzip not found. Please install unzip utility or 7-zip.
    exit /b 1
)

:: ------------------------------------------------------------------------------
:: Install Python Dependencies
:: ------------------------------------------------------------------------------
echo [%DATE% %TIME%] Installing Python requirements...
phishpedia_env\Scripts\python.exe -m pip install --upgrade pip
phishpedia_env\Scripts\python.exe -m pip install -r requirements.txt

:: ------------------------------------------------------------------------------
:: Install PyTorch (Required for Detectron2)
:: ------------------------------------------------------------------------------
echo [%DATE% %TIME%] Installing PyTorch and torchvision...
phishpedia_env\Scripts\python.exe -m pip install torch torchvision

:: ------------------------------------------------------------------------------
:: Install Detectron2 (Local Version)
:: ------------------------------------------------------------------------------
echo [%DATE% %TIME%] Installing detectron2 from local directory...
phishpedia_env\Scripts\python.exe -m pip install --no-build-isolation -e ..\detectron2 || (
    echo [ERROR] Failed to install detectron2 from local directory.
    echo [INFO] Make sure PyTorch is installed and detectron2 directory exists.
    exit /b 1
)

:: ------------------------------------------------------------------------------
:: Test Installation
:: ------------------------------------------------------------------------------
echo [%DATE% %TIME%] Testing installation...
phishpedia_env\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__)" || (
    echo [ERROR] PyTorch import failed!
    exit /b 1
)

phishpedia_env\Scripts\python.exe -c "import detectron2; print('Detectron2: OK')" || (
    echo [ERROR] Detectron2 import failed!
    exit /b 1
)

echo [SUCCESS] Core dependencies installed successfully!

:: ------------------------------------------------------------------------------
:: Setup Directories for Models
:: ------------------------------------------------------------------------------
set "FILEDIR=%cd%"
set "MODELS_DIR=%FILEDIR%\models"
if not exist "%MODELS_DIR%" mkdir "%MODELS_DIR%"
cd /d "%MODELS_DIR%"

:: ------------------------------------------------------------------------------
:: Download Model Files
:: ------------------------------------------------------------------------------
set RETRY_COUNT=3

:: Model files and Google Drive IDs
set file1=rcnn_bet365.pth
set id1=1tE2Mu5WC8uqCxei3XqAd7AWaP5JTmVWH

set file2=faster_rcnn.yaml
set id2=1Q6lqjpl4exW7q_dPbComcj0udBMDl8CW

set file3=resnetv2_rgb_new.pth.tar
set id3=1H0Q_DbdKPLFcZee8I14K62qV7TTy7xvS

set file4=expand_targetlist.zip
set id4=1fr5ZxBKyDiNZ_1B6rRAfZbAHBBoUjZ7I

set file5=domain_map.pkl
set id5=1qSdkSSoCYUkZMKs44Rup_1DPBxHnEKl1

:: ------------------------------------------------------------------------------
:: Download Loop
:: ------------------------------------------------------------------------------
for /L %%i in (1,1,5) do (
    call set "FILENAME=%%file%%i%%"
    call set "FILEID=%%id%%i%%"

    if exist "!FILENAME!" (
        echo [INFO] !FILENAME! already exists. Skipping.
    ) else (
        set /A count=1
        :retry_%%i
        echo [%DATE% %TIME%] Downloading !FILENAME! (Attempt !count!/%RETRY_COUNT%)...
        %FILEDIR%\phishpedia_env\Scripts\python.exe -m gdown --id !FILEID! -O "!FILENAME!" && goto downloaded_%%i

        set /A count+=1
        if !count! LEQ %RETRY_COUNT% (
            timeout /t 2 >nul
            goto retry_%%i
        ) else (
            echo [ERROR] Failed to download !FILENAME! after %RETRY_COUNT% attempts.
            exit /b 1
        )
        :downloaded_%%i
    )
)

:: ------------------------------------------------------------------------------
:: Extract Files
:: ------------------------------------------------------------------------------
echo [%DATE% %TIME%] Extracting expand_targetlist.zip...
unzip -o expand_targetlist.zip -d expand_targetlist || (
    echo [ERROR] Failed to unzip file.
    exit /b 1
)

:: Flatten nested folder if necessary
cd expand_targetlist
if exist expand_targetlist\ (
    echo [INFO] Flattening nested expand_targetlist directory...
    move expand_targetlist\*.* . >nul
    rmdir expand_targetlist
)

cd /d "%FILEDIR%"

:: ------------------------------------------------------------------------------
:: Final Test
:: ------------------------------------------------------------------------------
echo [%DATE% %TIME%] Testing Phishpedia imports...
phishpedia_env\Scripts\python.exe -c "from phishpedia import PhishpediaWrapper; print('Phishpedia import: OK')" || (
    echo [WARNING] Phishpedia import failed. Check if all models are downloaded.
)

:: ------------------------------------------------------------------------------
:: Success
:: ------------------------------------------------------------------------------
echo.
echo [%DATE% %TIME%] [SUCCESS] Setup completed successfully!
echo.
echo Next steps:
echo 1. Test with: phishpedia_env\Scripts\python.exe WEBtool\app.py
echo 2. Or use the manage-services.bat to start services
echo.
endlocal
pause
