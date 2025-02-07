# Bank Automation

Projekt automatyzacji operacji bankowych składający się z niezależnych modułów.

## Struktura projektu

<pre>
bank-automation/
├── src/
│   ├── email/        # moduł pobierania maili bankowych
│   ├── processing/    # moduł przetwarzania danych
│   └── utils/        # wspólne narzędzia
│
└── bank_statements/    # moduł obsługi wyciągów bankowych
    ├── config/        # konfiguracja i dane uwierzytelniające
    ├── data/
    │   ├── input_xml/  # pliki XML do przetworzenia
    │   └── processed_csv/ # przetworzone pliki CSV
    ├── logs/          # pliki logów
    └── src/          # kod źródłowy modułu
</pre>

## Moduły

### 1. Bank Statements Processor

Moduł do automatycznego przetwarzania wyciągów bankowych w formacie XML (CAMT52) i synchronizacji z Google Sheets.

* Parsowanie plików XML w standardzie ISO20022 (CAMT52)
* Konwersja transakcji bankowych z formatu XML na Google Sheets
* Integracja z Google Sheets
* System logowania
* Możliwość pobierania plików XML z Dysku Google

[Więcej informacji](bank_statements/README.md)

### 2. Email Processor (w przygotowaniu)

Moduł do automatycznego pobierania i przetwarzania maili bankowych.

## Konfiguracja

Każdy moduł ma własną konfigurację i wymagania. Szczegóły znajdują się w dokumentacji poszczególnych modułów.

## Wymagania systemowe

* Python 3.8+
* Git
* Dostęp do Google API (dla modułu bank_statements)
