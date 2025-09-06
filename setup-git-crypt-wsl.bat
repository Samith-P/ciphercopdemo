@echo off
echo 🔐 Git-Crypt Setup for CipherCop 2025 (WSL Version)
echo ====================================================

REM Check if WSL is available
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ WSL is not available!
    echo Please install Windows Subsystem for Linux first.
    pause
    exit /b 1
)

echo ✅ WSL is available

REM Check if git-crypt is installed in WSL
wsl git-crypt --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ git-crypt is not installed in WSL!
    echo Installing git-crypt in WSL...
    wsl sudo apt-get update
    wsl sudo apt-get install -y git-crypt
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to install git-crypt in WSL
        pause
        exit /b 1
    )
)

echo ✅ git-crypt is installed in WSL
wsl git-crypt --version

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ Not in a git repository!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo ✅ In git repository

REM Initialize git-crypt using WSL
echo.
echo 🔧 Initializing git-crypt...
wsl git-crypt init

if %errorlevel% equ 0 (
    echo ✅ git-crypt initialized successfully
) else (
    echo ❌ Failed to initialize git-crypt
    pause
    exit /b 1
)

REM Generate a key for the project using WSL
echo.
echo 🔑 Generating git-crypt key...
wsl git-crypt export-key ciphercop-git-crypt.key

if %errorlevel% equ 0 (
    echo ✅ Key exported to: ciphercop-git-crypt.key
    echo ⚠️  IMPORTANT: Keep this key file safe and secure!
    echo    - Share it securely with authorized team members
    echo    - Do NOT commit this key to the repository
) else (
    echo ❌ Failed to export key
    pause
    exit /b 1
)

REM Show status of encrypted files using WSL
echo.
echo 📊 Encrypted file status:
wsl git-crypt status

echo.
echo 🎉 Git-crypt setup completed!
echo.
echo 📋 Next steps:
echo    1. Add and commit the .gitattributes file
echo    2. Add and commit your .env files (they will be encrypted)
echo    3. Share ciphercop-git-crypt.key securely with team members
echo.
echo 🔓 To unlock files on a new machine:
echo    wsl git-crypt unlock ciphercop-git-crypt.key
echo.
echo 🔒 To lock files (optional):
echo    wsl git-crypt lock
echo.
echo 💡 Note: This setup uses WSL. All git-crypt commands should be prefixed with 'wsl'

pause
