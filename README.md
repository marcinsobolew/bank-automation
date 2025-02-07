### GŁÓWNY README (dla C:\Users\marci\bank-automation\README.md):

# Bank Automation 🏦

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

Kompleksowy system automatyzacji operacji bankowych. Projekt składa się z niezależnych modułów do przetwarzania wyciągów bankowych, analizy maili i automatyzacji operacji.

## 📋 Spis treści
- [Przegląd](#przegląd)
- [Struktura projektu](#struktura-projektu)
- [Moduły](#moduły)
- [Instalacja](#instalacja)
- [Wymagania](#wymagania-systemowe)
- [Rozwój projektu](#rozwój-projektu)

## 🔍 Przegląd
System składa się z niezależnych modułów, które można wykorzystywać osobno lub łączyć w kompleksowe rozwiązanie. Każdy moduł jest odpowiedzialny za konkretny aspekt automatyzacji operacji bankowych.

## 📁 Struktura projektu
bank-automation/
├── src/                      # główne źródła projektu
│   ├── email/               # moduł pobierania maili bankowych
│   ├── processing/          # moduł przetwarzania danych
│   └── utils/               # wspólne narzędzia
│
└── bank_statements/         # moduł obsługi wyciągów bankowych
    ├── config/              # konfiguracja i dane uwierzytelniające
    ├── data/               # dane wejściowe i wyjściowe
    │   ├── input_xml/      # pliki XML do przetworzenia
    │   └── processed_csv/  # przetworzone pliki CSV
    ├── logs/              # pliki logów
    └── src/               # kod źródłowy modułu

## 🔧 Moduły

### 1. Bank Statements Processor
![Status](https://img.shields.io/badge/Status-Active-green)

Moduł do automatycznego przetwarzania wyciągów bankowych w formacie XML i synchronizacji z Google Sheets.
- ✅ Parsowanie plików XML w standardzie ISO20022
- ✅ Integracja z Google Sheets
- ✅ System logowania

[Dokumentacja modułu](bank_statements/README.md)

### 2. Email Processor
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

Moduł do automatycznego pobierania i przetwarzania maili bankowych (w przygotowaniu).

## 🚀 Quick Start

1. Klonowanie repozytorium:
```bash
git clone https://github.com/marcinsobolew/bank-automation.git
cd bank-automation