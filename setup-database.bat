@echo off
echo ========================================
echo Setting Up PostgreSQL Database
echo ========================================
echo.

echo Starting PostgreSQL with Docker...
docker run -d ^
  --name fintech-postgres ^
  -e POSTGRES_USER=fintech ^
  -e POSTGRES_PASSWORD=fintech_secure_pass ^
  -e POSTGRES_DB=fintech ^
  -p 5432:5432 ^
  postgres:15-alpine

echo.
echo Waiting for PostgreSQL to start...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo PostgreSQL is ready!
echo ========================================
echo.
echo Connection Details:
echo   Host: localhost
echo   Port: 5432
echo   Database: fintech
echo   Username: fintech
echo   Password: fintech_secure_pass
echo.
echo Update your services to use this connection string:
echo postgresql://fintech:fintech_secure_pass@localhost:5432/fintech
echo.
pause
