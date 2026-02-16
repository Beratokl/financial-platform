@echo off
echo ========================================
echo Starting Financial Platform Services
echo ========================================
echo.

start "User Profile Service" cmd /k "cd /d %~dp0services\user-profile-service && python main-simple.py"
timeout /t 2 /nobreak >nul

start "Accounts Service" cmd /k "cd /d %~dp0services\accounts-service && python main-simple.py"
timeout /t 2 /nobreak >nul

start "Payments Service" cmd /k "cd /d %~dp0services\payments-service && python main-simple.py"
timeout /t 2 /nobreak >nul

start "Ledger Service" cmd /k "cd /d %~dp0services\ledger-service && python main-simple.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All Services Started!
echo ========================================
echo.
echo Open these URLs in your browser:
echo.
echo Users:    http://localhost:8004/docs
echo Accounts: http://localhost:8001/docs
echo Payments: http://localhost:8002/docs
echo Ledger:   http://localhost:8003/docs
echo.
echo Press any key to open dashboard...
pause >nul

start dashboard.html
