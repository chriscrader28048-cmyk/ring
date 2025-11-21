@echo off
chcp 65001 >nul
title He Thong Hen Gio Phat Am Thanh - LG Chem

:: Kiem tra quyen Admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Dang yeu cau quyen Administrator...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ============================================
echo    HE THONG HEN GIO PHAT AM THANH
echo    LG Chem - Made by Kitts
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

echo Dang khoi dong ung dung voi quyen Administrator...
echo.

python src\main_gui.py

echo.
echo Ung dung da dong. Nhan phim bat ky de thoat...
pause >nul
