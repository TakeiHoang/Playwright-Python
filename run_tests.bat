@echo off
REM Convenience test runner for Windows Command Prompt

echo ========================================================
echo Playwright UI & API Test Automation Suite
echo ========================================================
echo 1. Run All Smoke Tests (UI + API)
echo 2. Run UI Smoke Tests (Desktop)
echo 3. Run UI Smoke Tests (Mobile)
echo 4. Run API Smoke Tests
echo 5. Run UI Regression Tests (Desktop)
echo 6. Run UI Regression Tests (Mobile)
echo 7. Run API Regression Tests
echo 8. Run Complete Test Suite (All)
echo ========================================================

set /p choice="Enter choice [1-8]: "

if "%choice%"=="1" .\venv\Scripts\pytest.exe -m smoke
if "%choice%"=="2" .\venv\Scripts\pytest.exe -m "ui and smoke and desktop"
if "%choice%"=="3" .\venv\Scripts\pytest.exe -m "ui and smoke and mobile"
if "%choice%"=="4" .\venv\Scripts\pytest.exe -m "api and smoke"
if "%choice%"=="5" .\venv\Scripts\pytest.exe -m "ui and regression and desktop"
if "%choice%"=="6" .\venv\Scripts\pytest.exe -m "ui and regression and mobile"
if "%choice%"=="7" .\venv\Scripts\pytest.exe -m "api and regression"
if "%choice%"=="8" .\venv\Scripts\pytest.exe

pause
