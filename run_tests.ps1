<#
.SYNOPSIS
    Test execution runner for Playwright UI & API Test Framework.

.DESCRIPTION
    Runs tests categorized by suite (smoke/regression), test layer (ui/api),
    device (desktop/mobile), browser engine (chromium/firefox/webkit), and parallel workers.

.PARAMETER Type
    Target test layer: 'all', 'ui', or 'api'. Default is 'all'.

.PARAMETER Suite
    Target test suite: 'all', 'smoke', or 'regression'. Default is 'smoke'.

.PARAMETER Device
    Target device: 'desktop' or 'mobile'. Default is 'desktop'.

.PARAMETER Browser
    Target browser engine: 'chromium', 'firefox', 'webkit', or 'all'. Default is 'chromium'.

.PARAMETER Workers
    Number of parallel worker processes (e.g. '1', '2', '4', 'auto'). Default is '1'.

.PARAMETER Headed
    Run browser in headed (visible) mode instead of headless.

.PARAMETER HtmlReport
    Generate an HTML report at artifacts/report.html.

.EXAMPLE
    .\run_tests.ps1 -Type ui -Suite smoke -Browser all -Workers 3
    .\run_tests.ps1 -Type ui -Browser firefox -Device desktop
    .\run_tests.ps1 -Type ui -Browser webkit -Device mobile
    .\run_tests.ps1 -Suite smoke -Workers auto
#>

param (
    [ValidateSet("all", "ui", "api")]
    [string]$Type = "all",

    [ValidateSet("all", "smoke", "regression")]
    [string]$Suite = "smoke",

    [ValidateSet("desktop", "mobile")]
    [string]$Device = "desktop",

    [ValidateSet("chromium", "firefox", "webkit", "all")]
    [string]$Browser = "chromium",

    [string]$Workers = "1",

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
Write-Host "Browser:     $Browser" -ForegroundColor Yellow
Write-Host "Workers:     $Workers" -ForegroundColor Yellow
Write-Host "Marker:      $markerString" -ForegroundColor Yellow
Write-Host "Headed:      $($Headed.IsPresent)" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$pytestArgs = @()

# Marker filtering
if ($markerString) {
    $pytestArgs += "-m", "$markerString"
}

# Browser engines
if ($Browser -eq "all") {
    $pytestArgs += "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"
} else {
    $pytestArgs += "--browser", "$Browser"
}

# Parallel workers
if ($Workers -ne "1") {
    $pytestArgs += "-n", "$Workers"
}

# Headed mode
if ($Headed) {
    $pytestArgs += "--headed"
}

# Mobile emulation device
if ($Device -eq "mobile") {
    $pytestArgs += "--device=Pixel 5"
}

# HTML reporting
if ($HtmlReport) {
    New-Item -ItemType Directory -Force -Path "artifacts" | Out-Null
    $pytestArgs += "--html=artifacts/report.html", "--self-contained-html"
}

Write-Host "Executing: $PytestPath $($pytestArgs -join ' ')" -ForegroundColor Green
& $PytestPath @pytestArgs
