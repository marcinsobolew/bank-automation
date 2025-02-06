from file_processor import BankStatementProcessor
from sheets_manager import SheetsManager

def main():
    # ID arkusza Google Sheets (znajdziesz je w URL arkusza)
    SPREADSHEET_ID = '14Q_QqLkS8NFLY25oa1UsI7w6AL9NUYiGw9kGFOcrI9w'
    
    processor = BankStatementProcessor()
    sheets = SheetsManager()
    
    # Autoryzacja Google Sheets
    if not sheets.authenticate():
        print("Błąd autoryzacji Google Sheets")
        return

    # Przetwarzanie plików
    new_files = processor.get_new_files()
    if not new_files:
        print("Brak nowych plików do przetworzenia")
        return

    for file in new_files:
        print(f"Przetwarzanie pliku: {file}")
        if processor.process_file(file):
            print(f"Plik {file} został pomyślnie przetworzony")
            
            # Wczytaj przetworzone dane
            csv_path = os.path.join(processor.output_dir, 'all_transactions.csv')
            df = pd.read_csv(csv_path)
            
            # Wyślij do Google Sheets
            if sheets.update_sheet(df, SPREADSHEET_ID):
                print("Dane zostały zaktualizowane w Google Sheets")
            else:
                print("Błąd podczas aktualizacji Google Sheets")
        else:
            print(f"Błąd podczas przetwarzania pliku {file}")

if __name__ == "__main__":
    main()