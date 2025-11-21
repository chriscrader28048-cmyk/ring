@echo off
chcp 65001 >nul
title Dong Goi Ung Dung

echo ============================================
echo    DONG GOI UNG DUNG THANH FILE EXE
echo    LG Chem - Made by Kitts
echo ============================================
echo.

cd /d "%~dp0"

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Python chua duoc cai dat!
    pause
    exit /b 1
)

REM Cai dat PyInstaller neu chua co
echo Dang kiem tra PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Dang cai dat PyInstaller...
    pip install pyinstaller
)

echo.
echo Dang dong goi ung dung...
echo.

REM Dong goi thanh file exe
pyinstaller --noconfirm --onefile --windowed ^
    --name "LGChem_AudioScheduler" ^
    --icon "src/icon.ico" ^
    --add-data "src;src" ^
    --hidden-import pygame ^
    --hidden-import tkinter ^
    src/main_gui.py

if errorlevel 1 (
    REM Thu lai khong co icon
    pyinstaller --noconfirm --onefile --windowed ^
        --name "LGChem_AudioScheduler" ^
        --add-data "src;src" ^
        --hidden-import pygame ^
        --hidden-import tkinter ^
        src/main_gui.py
)

echo.
echo ============================================
if exist "dist\LGChem_AudioScheduler.exe" (
    echo    DONG GOI THANH CONG!
    echo    File: dist\LGChem_AudioScheduler.exe
) else (
    echo    CO LOI KHI DONG GOI!
)
echo ============================================
echo.

pause
