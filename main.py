# Script for receive mails from gmail and send its to vk chat
# Marakulin Andrey @annndruha
# 2020

import os
import time
import traceback
import datetime as dt

from gmail_module import auth, get_message, DATA_PATH
from vk_module import reconnect, write_msg, get_attach_str
from secret import config

SEND_LIST_PATH = './secret/sent_messages.txt'

def forward_message(service, new_msg_id):
    message_to_vk = get_message(service, new_msg_id) # Download attachments and extract message
    files = os.listdir(DATA_PATH)

    attachments_list = []
    error_counter = 0

    for file_name in files:
        attach_str = get_attach_str(config.user_id, DATA_PATH + file_name)
        if attach_str == 'error':
            error_counter +=1
        else:
            attachments_list.append(attach_str)

        os.remove(os.path.join(DATA_PATH, file_name))
    if len(attachments_list) > 0:
        attachment_ids = ','.join(attachments_list)
    else:
        attachment_ids = None

    if error_counter>0 : message_to_vk += f'\n<{error_counter}> вложений не загружено. Проверьте почту.'
    write_msg(config.user_id, message_to_vk, attach = attachment_ids)


if __name__ == '__main__':
    service = auth()
    reconnect()

    msg_id = service.users().messages().list(userId='me').execute()['messages'][0]['id'] # Select last id
    with open(SEND_LIST_PATH, 'w+') as f: # Create first time sent_messages file and add last message as send
        print(msg_id, file=f)

    print('===Script start===')
    start_time = time.time()
    while True:
        try:
            new_msg_id = service.users().messages().list(userId='me').execute()['messages'][0]['id']

            with open(SEND_LIST_PATH, 'r') as f:
                send_messages_ids = f.read().splitlines()

            if (msg_id != new_msg_id) and (new_msg_id not in send_messages_ids):
                forward_message(service, new_msg_id)
                msg_id = new_msg_id

                with open(SEND_LIST_PATH, 'a+') as f:
                    print(new_msg_id, file=f)

        except BaseException as err:
            traceback.print_tb(err.__traceback__)
            print(err.args)
            service = auth()
            reconnect()
            print(f"Smth wrong with message[{new_msg_id}] at {dt.datetime.strftime(dt.datetime.now(dt.timezone(dt.timedelta(hours = 3))), '[%d.%m.%Y %H:%M:%S]')}")
            msg_id = new_msg_id

        time.sleep(20.0 - ((time.time() - start_time) % 20.0))