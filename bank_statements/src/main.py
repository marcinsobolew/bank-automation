import os
import pandas as pd
from file_processor import BankStatementProcessor
from sheets_manager import SheetsManager
from drive_downloader import DriveDownloader
from logger import Logger

def main():
   logger = Logger()
   
   # ID arkusza Google Sheets
   SPREADSHEET_ID = '14Q_QqLkS8NFLY25oa1UsI7w6AL9NUYiGw9kGFOcrI9w'
   
   try:
       logger.info("Rozpoczęcie przetwarzania")
       
       # Pobieranie pliku z Google Drive
       drive_downloader = DriveDownloader()
       drive_downloader.authenticate()
       
       xml_file = drive_downloader.download_latest_xml()
       if not xml_file:
           logger.error("Nie udało się pobrać pliku XML z Google Drive")
           return
       
       processor = BankStatementProcessor()
       sheets = SheetsManager()
       
       # Autoryzacja Google Sheets
       if not sheets.authenticate():
           logger.error("Błąd autoryzacji Google Sheets")
           return
       
       # Test autoryzacji
       try:
           results = sheets.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
           logger.info(f"Nazwa arkusza: {results.get('properties', {}).get('title')}")
       except Exception as auth_test_error:
           logger.error(f"Błąd testu autoryzacji: {auth_test_error}")
           return
       
       # Przetwarzanie pobranego pliku
       try:
           logger.info(f"Przetwarzanie pliku: {xml_file}")
           
           if not processor.process_file(xml_file):
               logger.error(f"Błąd podczas przetwarzania pliku {xml_file}")
               return
           
           logger.info(f"Plik {xml_file} został pomyślnie przetworzony")
           
           # Wczytaj przetworzone dane
           csv_path = os.path.join(processor.output_dir, 'all_transactions.csv')
           df = pd.read_csv(csv_path)
           
           # Wyślij do Google Sheets
           if not sheets.update_sheet(df, SPREADSHEET_ID):
               logger.error("Błąd podczas aktualizacji Google Sheets")
               return
           
           logger.info("Dane zostały zaktualizowane w Google Sheets")
       
       except Exception as file_error:
           logger.error(f"Nieoczekiwany błąd podczas przetwarzania pliku: {file_error}")
   
   except Exception as main_error:
       logger.error(f"Krytyczny błąd w procesie głównym: {main_error}")
   
   finally:
       logger.info("Zakończenie przetwarzania")

if __name__ == "__main__":
   main()