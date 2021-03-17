from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# files import
import message as m

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_messages(service, users, mes, subject, attachments=None):
    print(users)

    for user in users:
        f = m.format_message(user[0], mes)
        s = m.format_message(user[0], subject)
        if attachments:
            formed_message = m.create_message_with_attachment(user[1], s, f, attachments)
            print("sending to: " + user[1])
            print("attachment: " + attachments.filename)
            m.send_message(service, "me", formed_message)
        else:
            formed_message = m.create_message(user[1], s, f)
            print("sending to: " + user[1])
            m.send_message(service, "me", formed_message)
    
    if attachments: attachments.close()
    
    

def start(users, message, subject, attachments=None):
    """
    Access Gmail API, get authentication or pickled token, and send emails.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    # use service
    send_messages(service, users, message, subject, attachments)


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)



if __name__ == '__main__':
    main()


