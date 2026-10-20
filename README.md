# 📱 Route POS Merchant & Collection App

[![Flet](https://img.shields.io/badge/UI-Flet%20(Flutter)-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flet.dev)
[![Android](https://img.shields.io/badge/Platform-Android%20%7C%20Desktop-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://flet.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A cross-platform Mobile & Desktop Point-of-Sale (POS) application built with **Flet (Python wrapper for Flutter)**, featuring Android compilation via Buildozer and an automated styled route dispatch Excel generator.

---

## 🌟 Features

- **Flutter-Powered Modern UI**: Smooth 60fps animations, dark mode aesthetics, and touch-optimized controls running on Windows, macOS, Linux, and Android.
- **Route Stop Sequence Selector**: Selects customer delivery stops dynamically from ERP route databases or offline datasets.
- **Collection Receipt Tracking**: Fast logging of cash, digital UPI, or returns credit directly on the delivery route.
- **Automated Dispatch Excel Sheet**: `route_sheet_generator.py` produces styled, formatted driver manifests with custom borders, headers, and column autofitting via `openpyxl`.
- **Android APK Ready**: Preconfigured with `buildozer.spec` for 1-click mobile APK compilation.

---

## 🚀 Quickstart

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run Desktop App
```bash
python app/main.py
```

### 3. Generate Styled Route Dispatch Sheet
```bash
python services/route_sheet_generator.py
```

### 4. Build Android APK (Linux / WSL)
```bash
pip install buildozer
buildozer android debug
```
The compiled APK will be output to `./bin/`.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Driver Delivery Stops] --> B[Flet Mobile / Desktop UI]
    B -->|Log Payment Receipt| C[Collection Feed]
    D[ERP Route DB / CSV] --> B
    D --> E[route_sheet_generator.py]
    E --> F[Styled Dispatch Excel Manifest]
    B -.->|buildozer.spec| G[Android .apk Package]
```

---

## 👨‍💻 Author
**Jose Anoob** — [GitHub Profile (@N0-DE)](https://github.com/N0-DE)
