from file_processor import BankStatementProcessor

def main():
    processor = BankStatementProcessor()
    
    new_files = processor.get_new_files()
    if not new_files:
        print("Brak nowych plików do przetworzenia")
        return

    for file in new_files:
        print(f"Przetwarzanie pliku: {file}")
        if processor.process_file(file):
            print(f"Plik {file} został pomyślnie przetworzony")
        else:
            print(f"Błąd podczas przetwarzania pliku {file}")

if __name__ == "__main__":
    main()