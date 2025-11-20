@echo off
chcp 65001 >nul
title Cap Nhat Tu GitHub

echo ============================================
echo    CAP NHAT PHAN MEM TU GITHUB
echo ============================================
echo.

cd /d "%~dp0"

echo Dang kiem tra ket noi...
git --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Git chua duoc cai dat!
    echo Vui long cai dat Git tu: https://git-scm.com/
    pause
    exit /b 1
)

echo Dang cap nhat tu GitHub...
git fetch origin
if errorlevel 1 (
    echo [LOI] Khong the ket noi den GitHub!
    echo Vui long kiem tra ket noi mang.
    pause
    exit /b 1
)

git pull origin main
if errorlevel 1 (
    git pull origin master
)

echo.
echo ============================================
echo    CAP NHAT HOAN TAT!
echo ============================================
echo.

echo Dang cap nhat cac thu vien Python...
pip install -r requirements.txt --quiet

echo.
echo Hoan tat! Nhan phim bat ky de dong...
pause >nul
