@echo off
REM ==========================================================
REM XE Tools Repository Download Batch File (No Git Required)
REM This script downloads the XE Tools repository as a ZIP file from GitHub,
REM extracts it into a folder, and then deletes the ZIP file.
REM ==========================================================

REM Set the URL to the repository ZIP file (assuming the main branch)
SET REPO_ZIP_URL=https://github.com/XynixDev/XE-tools/archive/refs/heads/main.zip
SET ZIP_FILE=XE-tools.zip
SET EXTRACT_FOLDER=XE-tools-main

echo Downloading repository ZIP from %REPO_ZIP_URL%...
powershell -Command "Invoke-WebRequest -Uri '%REPO_ZIP_URL%' -OutFile '%ZIP_FILE%'" 
IF ERRORLEVEL 1 (
    echo Failed to download repository ZIP. Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo Extracting ZIP file...
powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '.' -Force"
IF ERRORLEVEL 1 (
    echo Failed to extract ZIP file.
    pause
    exit /b 1
)

echo.
echo Deleting ZIP file...
del "%ZIP_FILE%"
echo.
echo Repository downloaded and extracted into folder: %EXTRACT_FOLDER%
pause
