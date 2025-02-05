import imaplib 
import email 
from email.header import decode_header 
import os 
from dotenv import load_dotenv 
 
class GmailConnector: 
    def __init__(self): 
        load_dotenv() 
        self.email_user = os.getenv('EMAIL_USER') 
        self.email_pass = os.getenv('EMAIL_PASSWORD') 
        self.bank_email = os.getenv('BANK_EMAIL') 
        self.imap_server = 'imap.gmail.com' 
 
    def connect(self): 
        try: 
            self.mail = imaplib.IMAP4_SSL(self.imap_server) 
            self.mail.login(self.email_user, self.email_pass) 
            print("Poˆ¥czono z Gmail") 
            return True 
        except Exception as e: 
            print(f"Bˆ¥d poˆ¥czenia: {e}") 
            return False 
