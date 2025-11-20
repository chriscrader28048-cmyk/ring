@echo off
chcp 65001 >nul
title Cai Dat Thu Vien

echo ============================================
echo    CAI DAT THU VIEN CAN THIET
echo ============================================
echo.

cd /d "%~dp0"

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Python chua duoc cai dat!
    echo.
    echo Vui long cai dat Python tu: https://python.org/
    echo Luu y: Tick vao "Add Python to PATH" khi cai dat.
    echo.
    pause
    exit /b 1
)

echo Python da duoc cai dat.
echo.

echo Dang cai dat cac thu vien can thiet...
echo.

pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ============================================
echo    CAI DAT HOAN TAT!
echo ============================================
echo.
echo Ban co the chay ung dung bang cach double-click vao file run.bat
echo.
pause
