@echo off
echo ========================================
echo Loading Sample Data into Platform
echo ========================================
echo.
echo This will create:
echo - 10 sample users
echo - 15 sample accounts
echo - 15 sample payments
echo - 15 ledger entries
echo.
pause

python populate-sample-data.py

echo.
echo ========================================
echo Done! Open demo.html to view the data
echo ========================================
pause
