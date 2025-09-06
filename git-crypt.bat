@echo off
REM Git-crypt wrapper for WSL
REM This allows using git-crypt as if it's installed natively on Windows

wsl git-crypt %*
