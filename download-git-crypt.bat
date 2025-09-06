@echo off
echo Git-Crypt Binary Download Helper
echo =================================
echo.

echo Since you have the source code but need the binary,
echo here are your options:
echo.

echo Option 1: Manual Download (Recommended)
echo ----------------------------------------
echo 1. Go to: https://github.com/AGWA/git-crypt/releases/latest
echo 2. Look for a file like: git-crypt-0.7.0-windows.zip
echo 3. Download and extract to C:\git-crypt\
echo.

echo Option 2: Use Pre-compiled Binary from Project
echo ----------------------------------------------
echo Some projects include pre-compiled binaries.
echo Let me check if there's one available online...
echo.

echo Creating a simple download using curl...
echo.

mkdir "C:\git-crypt" 2>nul

echo Attempting to download git-crypt binary...
echo Note: This may not work if the exact URL has changed
echo.

REM Try to download using built-in Windows tools
curl -L -o "C:\git-crypt\git-crypt.exe" "https://github.com/AGWA/git-crypt/releases/download/0.7.0/git-crypt.exe" 2>nul

if exist "C:\git-crypt\git-crypt.exe" (
    echo SUCCESS: Downloaded git-crypt.exe to C:\git-crypt\
    echo.
    echo Testing the downloaded binary...
    "C:\git-crypt\git-crypt.exe" --version
    echo.
    echo Next step: Add C:\git-crypt to your PATH
) else (
    echo Download failed or URL not available.
    echo.
    echo Please manually download from:
    echo https://github.com/AGWA/git-crypt/releases
    echo.
    echo Look for Windows binaries or compiled versions.
)

echo.
echo Alternative: Use WSL (Windows Subsystem for Linux)
echo --------------------------------------------------
echo If you have WSL installed, you can use:
echo   wsl sudo apt-get install git-crypt
echo   wsl git-crypt --version
echo.

pause
