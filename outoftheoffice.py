import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']

# Path to your credentials and token files
CREDENTIALS_PATH = 'C:\\Users\\ryan\\Documents\\Out of the Office\\credentials.json'
TOKEN_PATH = 'C:\\Users\\ryan\\Documents\\Out of the Office\\token.pickle'

def get_custom_message():
    """Prompt the user for a custom out-of-office message using Tkinter."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Default message crafted in a direct yet polite manner
    default_message = ("I understand you're reaching out and I appreciate your patience. "
                       "I'm currently unavailable but will address your message as soon as I return. "
                       "For immediate concerns, please call or text 587-888-5088. Thank you for understanding.")

    # Prompt the user for a custom message
    custom_message = simpledialog.askstring("Out-of-Office Message",
                                            "Enter your custom out-of-office message:",
                                            initialvalue=default_message)
    
    return custom_message if custom_message else default_message

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

    # Set the out-of-office message
    custom_message = get_custom_message()
    vacation_settings = {
        "enableAutoReply": True,
        "responseSubject": "Out of Office",
        "responseBodyPlainText": custom_message,
        "restrictToDomain": False,
        "restrictToContacts": False
    }

    try:
        service.users().settings().updateVacation(userId='me', body=vacation_settings).execute()
        messagebox.showinfo("Success", "Out-of-office message set successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set out-of-office message. Error: {e}")

if __name__ == '__main__':
    main()



sys.exit()
