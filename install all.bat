@echo off
REM ==========================================================
REM XE Tools Setup and Run Batch File
REM This script clones the XE Tools repository, installs all required Python packages,
REM and then runs the multitool (xe_tools.py).
REM ==========================================================

SET REPO_URL=https://github.com/XynixDev/XE-tools.git
SET REPO_DIR=XE-tools

echo Checking for Git...
git --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Git is not installed. Please install Git and then rerun this script.
    pause
    exit /b 1
)

IF NOT EXIST "%REPO_DIR%" (
    echo Cloning repository...
    git clone %REPO_URL%
    IF ERRORLEVEL 1 (
        echo Failed to clone repository. Please check your network connection.
        pause
        exit /b 1
    )
) ELSE (
    echo Repository already exists. Pulling the latest changes...
    pushd %REPO_DIR%
    git pull
    popd
)

echo.
echo Installing required Python packages...
pip install -r %REPO_DIR%\requirements.txt
IF ERRORLEVEL 1 (
    echo Failed to install dependencies. Please ensure pip is installed and try again.
    pause
    exit /b 1
)

echo.
echo Starting XE Tools multitool...
python %REPO_DIR%\xe_tools.py

pause
