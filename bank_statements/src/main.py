import os
import pandas as pd
from file_processor import BankStatementProcessor
from sheets_manager import SheetsManager
from logger import Logger

def main():
    logger = Logger()
    
    # ID arkusza Google Sheets
    SPREADSHEET_ID = '14Q_QqLkS8NFLY25oa1UsI7w6AL9NUYiGw9kGFOcrI9w'
    
    logger.info("Rozpoczęcie przetwarzania")
    
    processor = BankStatementProcessor()
    sheets = SheetsManager()
    
    # Autoryzacja Google Sheets
    if not sheets.authenticate():
        logger.error("Błąd autoryzacji Google Sheets")
        return

    # Przetwarzanie plików
    new_files = processor.get_new_files()
    if not new_files:
        logger.info("Brak nowych plików do przetworzenia")
        return

    for file in new_files:
        logger.info(f"Przetwarzanie pliku: {file}")
        if processor.process_file(file):
            logger.info(f"Plik {file} został pomyślnie przetworzony")
            
            # Wczytaj przetworzone dane
            csv_path = os.path.join(processor.output_dir, 'all_transactions.csv')
            df = pd.read_csv(csv_path)
            
            # Wyślij do Google Sheets
            if sheets.update_sheet(df, SPREADSHEET_ID):
                logger.info("Dane zostały zaktualizowane w Google Sheets")
            else:
                logger.error("Błąd podczas aktualizacji Google Sheets")
        else:
            logger.error(f"Błąd podczas przetwarzania pliku {file}")

    logger.info("Zakończenie przetwarzania")

if __name__ == "__main__":
    main()