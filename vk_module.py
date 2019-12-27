import requests
import json

from vk_api import VkApi
from vk_api.utils import get_random_id

from secret import config

vk = VkApi(token=config.access_token) # Auth with community token

def reconnect():
    """
    Reconnect to vk server
    """
    global vk
    vk = VkApi(token=config.access_token)


def get_attach_str(user_id, file_dir):
    """
    Upload files to vk server
    and return file id.
    """
    try:
        if (('.png' in file_dir) or ('.jpg' in file_dir)):
            getMessagesUploadServer = vk.method('photos.getMessagesUploadServer', {'peer_id': user_id})
            upload_url = getMessagesUploadServer['upload_url']
            file = {'photo': open(file_dir, 'rb')}

            ur = requests.post(upload_url, files= file).json()
            photo_metadata = vk.method('photos.saveMessagesPhoto',{'photo':ur['photo'], 'server':ur['server'], 'hash':ur['hash']})

            media_id = str(photo_metadata[0]['id'])
            owner_id = str(photo_metadata[0]['owner_id'])
            access_key = photo_metadata[0]['access_key']
            at = 'photo' + owner_id +'_'+media_id+'_'+access_key
        else:
            getMessagesUploadServer = vk.method('docs.getMessagesUploadServer', {'peer_id': user_id})
            upload_url = getMessagesUploadServer['upload_url']
            file = {'file': open(file_dir, 'rb')} # multipart/...data

            ur = requests.post(upload_url, files= file).json()
            file_metadata = vk.method('docs.save', {'file':ur['file']})

            media_id = str(file_metadata['doc']['id'])
            owner_id = str(file_metadata['doc']['owner_id'])
            at = 'doc' + owner_id +'_'+media_id
    except:
        at = 'error'
        return at
    else:
        return at


def write_msg(user_id, message=None, attach=None, parse_links = False):
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
    if parse_links == False:
        params['dont_parse_links']=1

    vk.method('messages.send', params)