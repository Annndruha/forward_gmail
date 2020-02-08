import requests
import json

from vk_api import VkApi
from vk_api.utils import get_random_id
config = json.load(open('./secret/config.json', 'r'))
vk = VkApi(token=config['access_token']) # Auth with community token

def reconnect():
    global vk # Reconnect to vk server
    vk = VkApi(token=config['access_token'])


def get_attach_str(user_id, file_dir):
    """
    Upload files to vk server
    and return file id string
    """
    try:
        if (('.png' in file_dir) or ('.jpg' in file_dir)):
            upload_url = vk.method('photos.getMessagesUploadServer', {'peer_id': user_id})['upload_url']
            file = {'photo': open(file_dir, 'rb')}

            ur = requests.post(upload_url, files= file).json()
            meta = vk.method('photos.saveMessagesPhoto',{'photo':ur['photo'], 'server':ur['server'], 'hash':ur['hash']})

            media_id = str(meta[0]['id'])
            owner_id = str(meta[0]['owner_id'])
            access_key = str(meta[0]['access_key'])
            at = f'photo{owner_id}_{media_id}_{access_key}'
        else:
            upload_url = vk.method('docs.getMessagesUploadServer', {'peer_id': user_id})['upload_url']
            file = {'file': open(file_dir, 'rb')} # multipart/...data (I fix this or not?)

            ur = requests.post(upload_url, files= file).json()
            meta = vk.method('docs.save', {'file':ur['file']})

            media_id = str(meta['doc']['id'])
            owner_id = str(meta['doc']['owner_id'])
            at = f'doc{owner_id}_{media_id}'
    except:
        return 'error'
    else:
        return at


def write_msg(user_id, message=None, attach=None, dont_parse_links = 1):
    """
    Write vk message. Must user_id. And need message or/and attach
    """
    params = {'user_id': user_id, 'random_id': get_random_id()}

    if message is not None and attach is not None:
        params['message']=message
        params['attachment']=attach
    elif message is not None and attach is None:
        params['message']=message
    elif message is None and attach is not None:
        params['attachment']=attach

    params['dont_parse_links']=dont_parse_links
    vk.method('messages.send', params)