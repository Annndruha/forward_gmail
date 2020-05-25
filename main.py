# Script for receive mails from gmail and send its to vk chat
# Marakulin Andrey @annndruha
# 2020
import os
import time
import traceback
import datetime as dt
import json

SEND_LIST_PATH = './secret/sent_messages.txt'
config = json.load(open('./secret/config.json', 'r'))

from gmail_module import auth, get_message, DATA_PATH
from vk_module import reconnect, write_msg, get_attach_str


def forward_message(service, new_msg_id):
    message_to_vk = get_message(service, new_msg_id) # Download attachments and extract message
    try:
        files = os.listdir(DATA_PATH)
    except FileNotFoundError:
        os.mkdir(DATA_PATH)
        files = os.listdir(DATA_PATH)

    attachments_list = []
    error_counter = 0

    for file_name in files:
        attach_str = get_attach_str(config['user_id'], DATA_PATH + file_name)
        if attach_str == 'error':
            error_counter +=1
        else:
            attachments_list.append(attach_str)

        os.remove(os.path.join(DATA_PATH, file_name))
    if len(attachments_list) > 0:
        attachment_ids = ','.join(attachments_list)
    else:
        attachment_ids = None

    if error_counter>0 : message_to_vk += f'\n<{error_counter} вложений не загружено. Проверьте почту.>'
    write_msg(config['user_id'], message_to_vk, attach = attachment_ids)



if __name__ == '__main__':
    service = auth()
    reconnect()

    last_msg_ids = service.users().messages().list(userId='me').execute()
    msg_id = last_msg_ids['messages'][0]['id'] # Select last id

    with open(SEND_LIST_PATH, 'a+') as f: # Create sent_messages before start moment file and add last message as send
        for i, mmm in enumerate(last_msg_ids['messages']):
            print(mmm['id'], file=f)

    print('===Script start===')
    while True:
        try:
            lbls = list().append('INBOX')
            response_msgs = service.users().messages().list(userId='me',labelIds=lbls).execute()

            new_msg_id =response_msgs['messages'][0]['id']

            with open(SEND_LIST_PATH, 'r') as f:
                send_messages_ids = f.read().splitlines()


            if (msg_id != new_msg_id) and (new_msg_id not in send_messages_ids):
                forward_message(service, new_msg_id)
                msg_id = new_msg_id

                with open(SEND_LIST_PATH, 'a+') as f:
                    print(new_msg_id, file=f)

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            print(err.args)
            service = auth()
            reconnect()
            print(f"Smth wrong with message[{new_msg_id}] at {dt.datetime.strftime(dt.datetime.now(dt.timezone(dt.timedelta(hours = 3))), '[%d.%m.%Y %H:%M:%S]')}")
            write_msg(config['user_id'], f"Smth wrong with message[{new_msg_id}] at {dt.datetime.strftime(dt.datetime.now(dt.timezone(dt.timedelta(hours = 3))), '[%d.%m.%Y %H:%M:%S]')}")
            msg_id = new_msg_id

        time.sleep(5)