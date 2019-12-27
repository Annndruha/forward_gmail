import requests
import json

from vk_api import VkApi
from vk_api.utils import get_random_id

from secret import config

vk = VkApi(token=config.access_token)# Auth with community token

def reconnect():
    global vk
    vk = VkApi(token=config.access_token)

def get_attach_str(user_id, type, file_dir):
    if type=='photo':
        getMessagesUploadServer = vk.method('photos.getMessagesUploadServer', {'peer_id': user_id})
        upload_url = getMessagesUploadServer['upload_url']
        file = {type: open(file_dir, 'rb')}

        ur = requests.post(upload_url, files= file).json()

        photo = vk.method('photos.saveMessagesPhoto',{'photo':ur['photo'], 'server':ur['server'], 'hash':ur['hash']})

        media_id = str(photo[0]['id'])
        owner_id = str(photo[0]['owner_id'])
        access_key = photo[0]['access_key']
        at = type + owner_id +'_'+media_id+'_'+access_key
        return at
    if type=='doc':
        getMessagesUploadServer = vk.method('docs.getMessagesUploadServer', {'peer_id': user_id})
        upload_url = getMessagesUploadServer['upload_url']
        file = {'file': open(file_dir, 'rb')} # multipart/...data

        ur = requests.post(upload_url, files= file).json()

        photo = vk.method('docs.save',{'file':ur['doc'], 'server':ur['server'], 'hash':ur['hash']})

        media_id = str(photo[0]['id'])
        owner_id = str(photo[0]['owner_id'])
        access_key = photo[0]['access_key']
        at = type + owner_id +'_'+media_id+'_'+access_key
        return at


def write_msg(user_id, message=None, attach=None, parse_links = False):
    params = {'user_id': user_id, 'random_id': get_random_id()}

    if message is not None and attach is not None:
        params['message']=message
        params['attachment']=attach
    elif message is not None and attach is None:
        params['message']=message
    elif message is None and attach is not None:
        params['attachment']=attach
    if parse_links == False:
        params['dont_parse_links']=1

    vk.method('messages.send', params)
