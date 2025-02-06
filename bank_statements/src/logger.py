import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logs_dir = os.path.join(base_dir, 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        # Konfiguracja loggera
        self.logger = logging.getLogger('BankStatements')
        self.logger.setLevel(logging.INFO)

        # Handler dla pliku
        log_file = os.path.join(logs_dir, f'bank_statements_{datetime.now().strftime("%Y%m")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Handler dla konsoli
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Format logów
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Dodaj handlery do loggera
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)