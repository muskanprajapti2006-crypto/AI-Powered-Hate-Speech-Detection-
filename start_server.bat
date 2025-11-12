@echo off
echo ======================================
echo Starting Hate Speech Detector Server
echo ======================================
echo.
echo Opening browser at http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

start http://localhost:5000
python app_server.py

pause
