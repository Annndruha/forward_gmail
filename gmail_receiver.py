


#from __future__ import print_function
import re
import os.path
import base64
import email

#from apiclient import errors
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def auth():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
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
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service


def GetAttachments(service, user_id, msg_id, store_dir, message):
    try:
        textExist = False
        for part in message['payload']['parts']:
            if part['filename']:

                att_id = part['body']['attachmentId']

                attach = service.users().messages().attachments().get(userId='me', messageId = msg_id, id=att_id).execute()
                data = attach['data']
                bytes = base64.urlsafe_b64decode(data.encode('UTF-8'))

                path = ''.join([store_dir, part['filename']])

                with open(path, 'wb') as f:
                    f.write(bytes)
                    f.close()
            else:
                data = part['body']['data']
                bytes = base64.urlsafe_b64decode(data.encode('UTF-8'))


                bad_text = bytes.decode('utf-8')
                cleanr = re.compile('<.*?>')
                cleantext = re.sub(cleanr, '', bad_text)

                path = ''.join([store_dir, 'plain_text.txt'])

                with open(path, 'w') as f:
                    f.write(cleantext)
                    f.close()
                textExist = True
                
        exitCode = 0
    except:
        exitCode = 1
    return exitCode, textExist


def GetSimpleText(message):
    data = message['payload']['body']['data']
    bytes = base64.urlsafe_b64decode(data.encode('UTF-8'))


    bad_text = bytes.decode('utf-8')
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', bad_text)
    if cleantext.find('&')>=0:
        cleantext = cleantext.split('&')[0]
        cleantext += '\nПродолжение читать в источнике...'
    return cleantext


if __name__ == '__main__':
    service = auth()

    messages_ids = service.users().messages().list(userId='me').execute() # Get messages ids
    msg_id = messages_ids['messages'][0]['id'] # Select last id
    message = service.users().messages().get(userId='me', id=msg_id).execute() # Get info about last message
    MIME_type = message['payload']['mimeType']

    theme = None
    sender = None
    for d in message['payload']['headers']:
        if d['name'] == 'Subject':
            theme = d['value']
        if d['name'] == 'From':
            sender = d['value']

    if MIME_type == 'multipart/mixed':
        exitCode, textExist = GetAttachments(service, 'me', msg_id, './data/', message)
        if textExist == True:
            with open('data/plain_text.txt', 'r') as f:
                text = f.read()
                f.close()
        else:
            text = '//Без текста//'
    elif MIME_type == 'text/html':
        text = GetSimpleText(message)
    elif MIME_type == 'text/plain':
        text = '//Без текста//'
    else:
        do_smth_else = 0

    message_to_vk = ''
    if sender is not None:
        message_to_vk += sender + '\n'
    if theme is not None:
        message_to_vk += theme + '\n'
    if text is not None:
        message_to_vk += text
    print(message_to_vk)