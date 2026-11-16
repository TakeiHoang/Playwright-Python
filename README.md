# Playwright Python UI & API Automation Framework

A production-ready test automation framework using **Playwright for Python**, **pytest**, and the **Page Object Model (POM)** pattern. Supports both **UI** (SauceDemo) and **API** (REST) testing with dedicated **Desktop** and **Mobile** emulation configurations, segmented by **Smoke** and **Regression** tags.

---

## 📁 Project Structure

```text
Playwright-Python/
├── .github/
│   └── workflows/
│       ├── main-pr-validation.yml      # CI Gatekeeper protecting 'main' branch
│       └── dependent-test-pipeline.yml # Staged pipeline with job dependencies
├── config/
│   ├── __init__.py
│   └── settings.py              # Centralized environment configs, URLs & credentials
├── pages/                       # Page Object Models (UI)
│   ├── __init__.py
│   ├── base_page.py             # Reusable base page methods (navigation, screenshots)
│   ├── login_page.py            # SauceDemo Login POM
│   ├── inventory_page.py        # SauceDemo Catalog & Products POM
│   ├── cart_page.py             # Shopping Cart POM
│   └── checkout_page.py         # Multi-step Checkout POM
├── api/                         # API Client Layer
│   ├── __init__.py
│   ├── base_api.py              # Playwright APIRequestContext client wrapper
│   ├── users_client.py          # Users CRUD endpoints client
│   └── auth_client.py           # Authentication endpoints client
├── tests/                       # Test Suites
│   ├── __init__.py
│   ├── conftest.py              # Desktop/Mobile fixtures, POM fixtures, API contexts
│   ├── ui/                      # Web UI Test Suite
│   │   ├── __init__.py
│   │   ├── test_auth.py         # Login, lockout & logout tests
│   │   ├── test_inventory.py    # Product listing, sorting & cart badge tests
│   │   └── test_checkout.py     # E2E purchase flow & validation tests
│   └── api/                     # REST API Test Suite
│       ├── __init__.py
│       ├── test_auth_api.py     # API login & registration tests
│       └── test_users_api.py    # API users CRUD tests
├── artifacts/                   # Test execution artifacts (screenshots, reports)
├── pytest.ini                   # Pytest configuration & registered markers
├── requirements.txt             # Project Python dependencies
├── run_tests.ps1                # PowerShell test runner script
├── run_tests.bat                # Windows CMD interactive batch launcher
└── README.md                    # Documentation
```

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+ (Python 3.11 - 3.15 supported)

### 2. Environment Setup

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
playwright install
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
playwright install
```

---

## 🏷️ Tagging System (Pytest Markers)

Tests are tagged with flexible, combinable markers registered in `pytest.ini`:

| Marker | Description | Scope |
| :--- | :--- | :--- |
| `@pytest.mark.smoke` | Fast, critical-path sanity tests (P0 flows) | UI & API |
| `@pytest.mark.regression` | Thorough functional validation and edge cases | UI & API |
| `@pytest.mark.ui` | Web browser user interface tests | SauceDemo |
| `@pytest.mark.api` | Backend REST API tests | ReqRes |
| `@pytest.mark.desktop` | Tests executed on 1920x1080 desktop browser | UI |
| `@pytest.mark.mobile` | Tests executed with mobile emulation (Pixel 5 / iPhone) | UI |

---

## 💻 Running Tests by Tags

### 1. Smoke Tests
```bash
# Run all smoke tests (both UI and API)
pytest -m smoke

# Run UI smoke tests only (Desktop + Mobile)
pytest -m "ui and smoke"

# Run UI smoke tests on Desktop only
pytest -m "ui and smoke and desktop"

# Run UI smoke tests on Mobile only
pytest -m "ui and smoke and mobile"

# Run API smoke tests only
pytest -m "api and smoke"
```

### 2. Regression Tests
```bash
# Run all regression tests (both UI and API)
pytest -m regression

# Run UI regression tests only
pytest -m "ui and regression"

# Run Desktop UI regression tests
pytest -m "ui and regression and desktop"

# Run Mobile UI regression tests
pytest -m "ui and regression and mobile"

# Run API regression tests
pytest -m "api and regression"
```

### 3. Device-Specific Runs
```bash
# Run all desktop UI tests
pytest -m "ui and desktop"

# Run all mobile UI tests
pytest -m "ui and mobile"

# Override mobile emulation device on the fly
pytest -m "ui and mobile" --device="iPhone 13"
```

---

## 🌐 Multi-Browser Testing (Chrome, Firefox, WebKit)

The framework dynamically launches tests across all 3 major Playwright browser engines:

```bash
# Run on Chromium (Google Chrome engine - default)
pytest -m "ui and smoke" --browser chromium

# Run on Firefox (Mozilla engine)
pytest -m "ui and smoke" --browser firefox

# Run on WebKit (Apple Safari engine)
pytest -m "ui and smoke" --browser webkit

# Run simultaneously across ALL 3 browser engines!
pytest -m "ui and smoke" --browser chromium --browser firefox --browser webkit
```

---

## ⚡ Multi-Worker Parallel Execution (`pytest-xdist`)

Speed up test execution by distributing tests across multiple CPU workers:

```bash
# Run with 3 parallel workers
pytest -m "ui and smoke" -n 3

# Run on all 3 browsers simultaneously across 3 parallel workers
pytest -m "ui and smoke" --browser chromium --browser firefox --browser webkit -n 3

# Automatically scale workers to all available CPU cores
pytest -m regression -n auto
```

---

## 🛠️ Convenience Runners

### PowerShell Script (`run_tests.ps1`)
```powershell
# Run UI Smoke tests on Desktop
.\run_tests.ps1 -Type ui -Suite smoke -Device desktop

# Run Mobile UI Smoke tests
.\run_tests.ps1 -Type ui -Suite smoke -Device mobile

# Run API Regression tests
.\run_tests.ps1 -Type api -Suite regression

# Run with visible browser (headed) and generate HTML report
.\run_tests.ps1 -Type ui -Suite smoke -Device desktop -Headed -HtmlReport
```

### Windows Batch Launcher (`run_tests.bat`)
Double-click `run_tests.bat` or run from cmd for an interactive 1-click test selector.

---

## 🧩 Architecture Details

### Page Object Model (POM)
Every page is modeled with a dedicated class inheriting from `BasePage`:
- **`LoginPage`**: Enforces login flows, error states (`locked_out_user`, missing credentials).
- **`InventoryPage`**: Encapsulates product listings, dynamic sorting (`lohi`, `za`), mobile hamburger drawer menu, and cart updates.
- **`CartPage`**: Handles item verification and removal.
- **`CheckoutPage`**: Controls multi-step customer details, order summary calculations, and order confirmation.

### Intelligent `app_page` Fixture
The `app_page` fixture inspects pytest markers at runtime:
- Tests marked with `@pytest.mark.mobile` automatically receive a mobile viewport context (`Pixel 5` / `iPhone 13` touch & dimensions).
- Tests marked with `@pytest.mark.desktop` receive a full `1920x1080` desktop context.
- Can be overridden via CLI with `--device="<Device Name>"`.

### API Client Architecture
The API layer leverages Playwright's native `APIRequestContext`:
- `BaseApiClient` handles base URLs, JSON serialization, headers, and HTTP verbs.
- `UsersApiClient` manages user CRUD operations.
- `AuthApiClient` handles login/registration payload validations.
- Runs without launching a browser, providing lightning-fast API test execution.

### Failure Diagnostics
In case of any test failure:
- Pytest hooks automatically capture a full-page screenshot of the application state.
- Screenshots are saved under `artifacts/failures/<test_name>.png`.

---

## 🤖 GitHub Actions CI/CD Workflows

### 1. Main Branch Integrity & PR Gatekeeper (`.github/workflows/main-pr-validation.yml`)
Ensures no broken code reaches the `main` branch:
- **Triggers**: On pull requests targeting `main` and pushes directly to `main`.
- **Pipeline Architecture with Job Dependencies (`needs:`)**:
  ```text
  [1. Code Integrity & Syntax Check]
         │
         ├──> [2. API Smoke Gate] ──────┐
         │                              │
         ├──> [3. UI Desktop Smoke Gate]├──> [5. Main Merge Protection Gatekeeper]
         │                              │
         └──> [4. UI Mobile Smoke Gate] ─┘
  ```
- **Merge Protection**: Set `5. Main Merge Protection Gatekeeper` as a required status check in GitHub Branch Protection rules.

### 2. Dependent Staged Test Pipeline (`.github/workflows/dependent-test-pipeline.yml`)
Demonstrates cascading, sequential job dependencies:
- **Triggers**: Nightly schedule at 02:00 UTC and on-demand via `workflow_dispatch`.
- **Sequential Stages**:
  ```text
  Stage 1: Pre-flight Verification
    │ (needs: stage1)
    ▼
  Stage 2: API Smoke Sanity
    │ (needs: stage2)
    ▼
  Stage 3: UI Smoke Matrix (Desktop & Mobile)
    │ (needs: stage3)
    ▼
  Stage 4: Comprehensive Regression Suite
    │ (needs: all prior)
    ▼
  Stage 5: Pipeline Status Summary & Reporting
  ```
- Downstream stages only execute if upstream prerequisites pass, preventing wasted browser runner minutes when upstream API or smoke checks fail.
