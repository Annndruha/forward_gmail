# Script for receive mails from gmail and send its to vk chat
# Marakulin Andrey @annndruha
# 2020
import os

from gmail_module import auth, get_message
from vk_module import reconnect, write_msg, get_attach_str
from secret import config

if __name__ == '__main__':
    service = auth()

    messages_ids = service.users().messages().list(userId='me').execute() # Get messages ids
    msg_id = messages_ids['messages'][0]['id'] # Select last id
    message_to_vk = get_message(service, msg_id)

    dir = './data/'
    files = os.listdir(dir)
    attachments_list = []
    for file_name in files:
        if (('.png' in file_name) or ('.jpg' in file_name)):
            attach_str = get_attach_str(config.user_id, 'photo', dir+file_name)
            attachments_list.append(attach_str)
            os.remove(os.path.join(dir, file_name))
        else:
            attach_str = get_attach_str(config.user_id, 'doc', dir+file_name)
            attachments_list.append(attach_str)
            os.remove(os.path.join(dir, file_name))

    
    write_msg(config.user_id, message_to_vk, attach=attach_str)
    #print(message_to_vk)