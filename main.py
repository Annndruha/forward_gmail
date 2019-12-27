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


def forward_message(service, new_msg_id):
    message_to_vk = get_message(service, new_msg_id) # Download attachments and extract message
    files = os.listdir(DATA_PATH)
    attachments_list = []

    for file_name in files:
        attach_str = get_attach_str(config.user_id, DATA_PATH + file_name)
        if attach_str == 'error':
            message_to_vk += '\nОдно или несколько вложений не загружено. Проверьте почту.'
        else:
            attachments_list.append(attach_str)
        os.remove(os.path.join(DATA_PATH, file_name))
    if len(attachments_list) > 0:
        attachment_ids = ','.join(attachments_list)
    else:
        attachment_ids = None

    write_msg(config.user_id, message_to_vk, attach = attachment_ids)



if __name__ == '__main__':
    service = auth()
    reconnect()

    messages_ids = service.users().messages().list(userId='me').execute() # Get messages ids
    msg_id = messages_ids['messages'][0]['id'] # Select last id
    

    new_msg_id = None
    print('===Script start===')
    start_time = time.time()
    while True:
        try:
            messages_ids = service.users().messages().list(userId='me').execute()
            new_msg_id = messages_ids['messages'][0]['id']

            if msg_id != new_msg_id:
                forward_message(service, new_msg_id)
                msg_id = new_msg_id

        except BaseException as err:
            traceback.print_tb(err.__traceback__)
            print(err.args)
            service = auth()
            reconnect()
            print(f"Message [{new_msg_id}] not sent at {dt.datetime.strftime(dt.datetime.now(dt.timezone(dt.timedelta(hours = 3))), '[%d.%m.%Y %H:%M:%S]')}")
            msg_id = new_msg_id

        time.sleep(20.0 - ((time.time() - start_time) % 20.0))