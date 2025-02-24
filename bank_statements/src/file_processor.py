import os
import pandas as pd
import xml.etree.ElementTree as ET

class BankStatementProcessor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.input_dir = os.path.join(base_dir, 'data', 'input_xml')
        self.output_dir = os.path.join(base_dir, 'data', 'processed_csv')
        self.processed_file = os.path.join(base_dir, 'data', 'processed_files.txt')
        self.ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02'}

    def get_new_files(self):
        processed_files = set()
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                processed_files = set(f.read().splitlines())
        
        all_files = set(os.listdir(self.input_dir))
        return all_files - processed_files

    def process_file(self, filename):
        try:
            tree = ET.parse(os.path.join(self.input_dir, filename))
            root = tree.getroot()
            
            transactions = []
            for entry in root.findall('.//ns:Ntry', self.ns):
                transaction = {}
                transaction['amount'] = float(entry.find('ns:Amt', self.ns).text)
                credit_debit = entry.find('ns:CdtDbtInd', self.ns).text
                transaction['amount'] = transaction['amount'] if credit_debit == 'CRDT' else -transaction['amount']
                
                booking_date = entry.find('.//ns:BookgDt/ns:Dt', self.ns).text
                transaction['date'] = booking_date
                
                details = entry.find('.//ns:TxDtls', self.ns)
                if details is not None:
                    cdtr = details.find('.//ns:Cdtr/ns:Nm', self.ns)
                    dbtr = details.find('.//ns:Dbtr/ns:Nm', self.ns)
                    transaction['counterparty'] = (cdtr.text if cdtr is not None else dbtr.text if dbtr is not None else 'BRAK')
                    
                    rmtinf = details.find('.//ns:RmtInf/ns:Ustrd', self.ns)
                    transaction['description'] = rmtinf.text if rmtinf is not None else ''

                transactions.append(transaction)

            df_new = pd.DataFrame(transactions)
            csv_path = os.path.join(self.output_dir, 'all_transactions.csv')
            
            if os.path.exists(csv_path):
                df_existing = pd.read_csv(csv_path)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined = df_combined.drop_duplicates()
                df_combined.to_csv(csv_path, index=False)
            else:
                df_new.to_csv(csv_path, index=False)

            with open(self.processed_file, 'a') as f:
                f.write(f"{filename}\n")

            return True

        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {filename}: {e}")
            return False