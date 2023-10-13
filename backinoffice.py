import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import tkinter as tk
from tkinter import messagebox
import sys

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']

# Path to your credentials and token files
CREDENTIALS_PATH = 'credentials.json'
TOKEN_PATH = 'token.pickle'

def main():
    creds = None

    # Check if token.pickle exists
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Set the out-of-office message to off
    vacation_settings = {
        "enableAutoReply": False,
    }

    try:
        service.users().settings().updateVacation(userId='me', body=vacation_settings).execute()
        messagebox.showinfo("Success", "Out-of-office message turned off successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to turn off out-of-office message. Error: {e}")

if __name__ == '__main__':
    main()
    
sys.exit()
