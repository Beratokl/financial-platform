@echo off
echo ========================================
echo Pushing to GitHub
echo ========================================
echo.

cd c:\Users\User\Financial_platform

echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Committing changes...
git commit -m "Initial commit: Financial Platform with microservices, frontend, and AWS deployment"

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Create a new repository on GitHub
echo 2. Copy the repository URL
echo 3. Run these commands:
echo.
echo    git remote add origin YOUR_GITHUB_URL
echo    git branch -M main
echo    git push -u origin main
echo.
pause
