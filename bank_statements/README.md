# Bank Statements Processor

Moduł do automatycznego przetwarzania wyciągów bankowych w formacie XML i synchronizacji z Google Sheets.

## Funkcjonalności

### 1. Przetwarzanie plików XML
- Automatyczne wykrywanie nowych plików XML w folderze `data/input_xml`
- Parsowanie standardu ISO20022 (format camt.053)
- Zapisywanie przetworzonych danych do CSV

### 2. Integracja z Google Sheets
- Automatyczna synchronizacja z arkuszem Google
- Autoryzacja OAuth 2.0
- Aktualizacja danych w czasie rzeczywistym

### 3. System logowania
- Logowanie do plików miesięcznych w folderze `logs/`
- Różne poziomy logów (INFO, ERROR, WARNING)
- Równoczesne logowanie do konsoli i pliku

## Struktura projektu

<pre>
bank_statements/
├── config/             # Konfiguracja i dane uwierzytelniające
│   └── credentials.json  # Dane dostępowe do Google API
├── data/               # Dane wejściowe i wyjściowe
│   ├── input_xml/      # Pliki XML do przetworzenia
│   └── processed_csv/   # Przetworzone pliki CSV
├── logs/               # Pliki logów
└── src/                # Kod źródłowy
    ├── file_processor.py  # Przetwarzanie plików XML
    ├── sheets_manager.py # Integracja z Google Sheets
    ├── logger.py        # System logowania
    └── main.py          # Główny skrypt
</pre>

## Konfiguracja i uruchomienie

1. Instalacja zależności:
pip install -r requirements.txt

2. Konfiguracja:
- Umieść plik `credentials.json` w folderze `config/`
- Skonfiguruj ID arkusza Google Sheets w `src/main.py`

3. Użycie:
- Umieść pliki XML w folderze `data/input_xml`
- Uruchom:
python src/main.py

## System logowania

Format logów:
YYYY-MM-DD HH:MM:SS - LEVEL - Message

Przykład:
2025-02-06 15:30:45 - INFO - Rozpoczęcie przetwarzania
2025-02-06 15:30:46 - INFO - Znaleziono nowy plik: export20250204.xml
2025-02-06 15:30:47 - INFO - Zakończono przetwarzanie pliku
