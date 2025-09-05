@echo off
setlocal enabledelayedexpansion

:: Git-Crypt Setup Script for CipherCop 2025 (Windows)
:: This script initializes git-crypt for protecting sensitive environment files

echo 🔐 Git-Crypt Setup for CipherCop 2025
echo ======================================

:: Check if git-crypt is installed
where git-crypt >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ git-crypt is not installed in PATH!
    echo.
    echo 📥 Adding git-crypt to PATH for this session...
    set "PATH=%PATH%;C:\git-crypt"
    echo ✅ git-crypt is now available via WSL wrapper
) else (
    echo ✅ git-crypt is already installed
)

:: Check if we're in a git repository
if not exist ".git" (
    echo ❌ Not in a git repository!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo ✅ In git repository

:: Initialize git-crypt
echo.
echo 🔧 Initializing git-crypt...
git-crypt init

if %errorlevel% equ 0 (
    echo ✅ git-crypt initialized successfully
) else (
    echo ❌ Failed to initialize git-crypt
    pause
    exit /b 1
)

:: Generate a key for the project
echo.
echo 🔑 Generating git-crypt key...
git-crypt export-key ciphercop-git-crypt.key

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

:: Show status of encrypted files
echo.
echo 📊 Encrypted file status:
git-crypt status

echo.
echo 🎉 Git-crypt setup completed!
echo.
echo 📋 Next steps:
echo    1. Add and commit the .gitattributes file
echo    2. Add and commit your .env files (they will be encrypted)
echo    3. Share ciphercop-git-crypt.key securely with team members
echo.
echo 🔓 To unlock files on a new machine:
echo    git-crypt unlock ciphercop-git-crypt.key
echo.
echo 🔒 To lock files (optional):
echo    git-crypt lock

pause
