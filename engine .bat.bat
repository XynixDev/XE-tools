@echo off
echo ============================================
echo       Starting Engine Simulation...
echo ============================================
echo.
echo Calling Engine_Start...
rundll32.exe EngineSimulator.dll,Engine_Start
echo.
echo Waiting for simulation to run...
timeout /t 5 /nobreak >nul
echo.
echo Getting Engine RPM...
rundll32.exe EngineSimulator.dll,Engine_GetRPM
echo.
echo Getting Engine Temperature...
rundll32.exe EngineSimulator.dll,Engine_GetTemperature
echo.
echo Stopping Engine Simulation...
rundll32.exe EngineSimulator.dll,Engine_Stop
echo.
echo ============================================
echo       Engine Simulation Completed
echo ============================================
pause
