# Gmail Forwarder
Script detect new Gmail messages and forward it's to VK chat (with attachments).

### First time setting:
+ Create (if not exist folder ```secret``` and ``temp`` in main directory)

+ Create or change file config.py in secret with:
```
access_token = 'your token'
group_id = 123456789
user_id = 123456789
```

+ Download a credentials file from: (Enable API)
https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the
and locate file to secret folder.

+ Run ```main.py``` First run it create a ```token.pickle``` in secret.
If you want to change settings in future, delete this file and repeat.

### Docker run

Run docker command:

```
docker run -d --name gmail -v /root/gmail/secret:/gmail/secret imagename
```