@echo off
chcp 65001 >nul
title Quan Ly Phat Am Thanh Theo Lich

echo ============================================
echo    QUAN LY PHAT AM THANH THEO LICH
echo ============================================
echo.

cd /d "%~dp0"

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Python chua duoc cai dat!
    echo Vui long cai dat Python tu: https://python.org/
    pause
    exit /b 1
)

REM Kiem tra va cai dat thu vien
echo Dang kiem tra thu vien can thiet...
pip show pygame >nul 2>&1
if errorlevel 1 (
    echo Dang cai dat thu vien...
    pip install -r requirements.txt --quiet
)

echo Dang khoi dong ung dung...
echo.

python src\main_gui.py

echo.
echo Ung dung da dong. Nhan phim bat ky de thoat...
pause >nul
