<#
.SYNOPSIS
    Test execution runner for Playwright UI & API Test Framework.

.DESCRIPTION
    Runs tests categorized by suite (smoke/regression), test layer (ui/api), and device (desktop/mobile).

.PARAMETER Type
    Target test layer: 'all', 'ui', or 'api'. Default is 'all'.

.PARAMETER Suite
    Target test suite: 'all', 'smoke', or 'regression'. Default is 'smoke'.

.PARAMETER Device
    Target device: 'desktop' or 'mobile'. Default is 'desktop'.

.PARAMETER Headed
    Run browser in headed (visible) mode instead of headless.

.PARAMETER HtmlReport
    Generate an HTML report at artifacts/report.html.

.EXAMPLE
    .\run_tests.ps1 -Type ui -Suite smoke -Device desktop
    .\run_tests.ps1 -Type api -Suite regression
    .\run_tests.ps1 -Suite smoke
    .\run_tests.ps1 -Device mobile -Suite regression -Headed
#>

param (
    [ValidateSet("all", "ui", "api")]
    [string]$Type = "all",

    [ValidateSet("all", "smoke", "regression")]
    [string]$Suite = "smoke",

    [ValidateSet("desktop", "mobile")]
    [string]$Device = "desktop",

    [switch]$Headed,
    [switch]$HtmlReport
)

# Ensure virtual environment python/pytest is used
$PytestPath = ".\venv\Scripts\pytest.exe"
if (-not (Test-Path $PytestPath)) {
    $PytestPath = "pytest"
}

# Construct pytest marker expression
$markerExpr = @()

if ($Suite -ne "all") {
    $markerExpr += $Suite
}

if ($Type -ne "all") {
    $markerExpr += $Type
}

# If UI tests are included, match device tag as well
if ($Type -eq "ui" -or ($Type -eq "all" -and $Suite -ne "all")) {
    if ($Device -eq "mobile") {
        $markerExpr += "mobile"
    } elseif ($Device -eq "desktop") {
        $markerExpr += "desktop"
    }
}

$markerString = $markerExpr -join " and "

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Playwright UI & API Test Automation Runner" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Type:        $Type" -ForegroundColor Yellow
Write-Host "Suite:       $Suite" -ForegroundColor Yellow
Write-Host "Device:      $Device" -ForegroundColor Yellow
Write-Host "Marker:      $markerString" -ForegroundColor Yellow
Write-Host "Headed:      $($Headed.IsPresent)" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$pytestArgs = @()

if ($markerString) {
    $pytestArgs += "-m", "$markerString"
}

if ($Headed) {
    $pytestArgs += "--headed"
}

if ($Device -eq "mobile") {
    $pytestArgs += "--device=Pixel 5"
}

if ($HtmlReport) {
    New-Item -ItemType Directory -Force -Path "artifacts" | Out-Null
    $pytestArgs += "--html=artifacts/report.html", "--self-contained-html"
}

Write-Host "Executing: $PytestPath $($pytestArgs -join ' ')" -ForegroundColor Green
& $PytestPath @pytestArgs
