@echo off
REM Convenience test runner for Windows Command Prompt

echo ========================================================
echo Playwright UI & API Test Automation Suite
echo ========================================================
echo 1. Run All Smoke Tests (Chrome)
echo 2. Run UI Smoke on Multi-Browser (Chrome + Firefox + WebKit)
echo 3. Run UI Smoke Parallel (Chrome + Firefox + WebKit with 3 Workers)
echo 4. Run UI Smoke (Firefox only)
echo 5. Run UI Smoke (WebKit only)
echo 6. Run API Smoke Tests (0 browsers, pure HTTP)
echo 7. Run Full Regression on All Browsers (Parallel workers)
echo 8. Run All Tests
echo ========================================================

set /p choice="Enter choice [1-8]: "

if "%choice%"=="1" .\venv\Scripts\pytest.exe -m smoke --browser chromium
if "%choice%"=="2" .\venv\Scripts\pytest.exe -m "ui and smoke" --browser chromium --browser firefox --browser webkit
if "%choice%"=="3" .\venv\Scripts\pytest.exe -m "ui and smoke" --browser chromium --browser firefox --browser webkit -n 3
if "%choice%"=="4" .\venv\Scripts\pytest.exe -m "ui and smoke" --browser firefox
if "%choice%"=="5" .\venv\Scripts\pytest.exe -m "ui and smoke" --browser webkit
if "%choice%"=="6" .\venv\Scripts\pytest.exe -m "api and smoke"
if "%choice%"=="7" .\venv\Scripts\pytest.exe -m regression --browser chromium --browser firefox --browser webkit -n auto
if "%choice%"=="8" .\venv\Scripts\pytest.exe

pause
