import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import sys
import os

# Setup logging to console
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def test_connection():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Check key file
    if not os.path.exists("service_account.json"):
        print("CRITICAL: service_account.json not found!")
        return

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)
        
        # User's ID from the link: 1cljWdPNFUtkLeMXzsyRP8dMAOaplaj9r8b5r_pdGMZw
        sheet_id = "1cljWdPNFUtkLeMXzsyRP8dMAOaplaj9r8b5r_pdGMZw"
        print(f"Testing connection to ID: {sheet_id}")

        spreadsheet = client.open_by_key(sheet_id)
        print(f"SUCCESS: Connected to '{spreadsheet.title}'")
        print(f"Spreadsheet ID: {spreadsheet.id}")
        
        # Try to read
        print("Attempting to read Sheet1...")
        sheet = spreadsheet.sheet1
        print(f"Ref successful: {sheet}")
        
    except Exception as e:
        print("\n--- FAILURE REPORT ---")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        
        if "400" in str(e) and "operation is not supported" in str(e):
            print("\nDIAGNOSIS: CONFIRMED EXCEL FILE")
            print("The ID belongs to an .xlsx file, NOT a Google Sheet.")
            print("Gspread cannot edit .xlsx files. It MUST be converted.")
        elif "403" in str(e):
             print("\nDIAGNOSIS: PERMISSION DENIED")
             print("The service account email was not added as an Editor.")

if __name__ == "__main__":
    test_connection()
