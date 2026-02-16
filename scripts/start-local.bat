@echo off
echo Starting Financial Platform...
echo.

echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed or not running
    exit /b 1
)

echo Starting services with Docker Compose...
docker-compose up -d postgres keycloak kafka zookeeper

echo Waiting for services to be ready...
timeout /t 30 /nobreak >nul

echo Building custom microservices...
docker-compose build

echo Starting all services...
docker-compose up -d

echo.
echo ========================================
echo Financial Platform is starting!
echo ========================================
echo.
echo Services:
echo - Keycloak: http://localhost:8080
echo - Fineract: https://localhost:8443
echo - Accounts Service: http://localhost:8001
echo - Payments Service: http://localhost:8002
echo - Ledger Service: http://localhost:8003
echo - User Profile Service: http://localhost:8004
echo.
echo Run 'docker-compose logs -f' to view logs
echo Run 'docker-compose down' to stop all services
