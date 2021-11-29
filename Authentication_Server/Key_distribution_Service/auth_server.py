'''
    - Authentication Server
'''
from datetime import datetime
import json
from hashlib import md5
from utils.RC4 import RC4

TGS_SECRET_KEY = 'EXAMPLE-TGS-SECRET-KEY'
VALID_P = '10'

def hash(text):
    data = text.encode('ascii', 'ignore')
    return md5(data).hexdigest()
    
users = {
    "alice":{
        "secret":hash("Alice_pswd"),
        "date_joined": datetime.today()
    }, 
    "bob":{
        "secret":hash("Bob_pswd"),
        "date_joined":datetime.now()
    }
}

def save_users(users):
    ''' Dumps dict into users.json file '''
    with open("users.json", "w") as outfile:
        json.dump(users, outfile,indent=4, default=str)
        

def get_users():
    '''
        returns data contained in users.json file
    '''
    f = open("users.json")
    users = json.load(f)
    f.close()
    return users

def user_details(username):
    f = open('users.json')
    users = json.load(f)
    f.close()
    if users[username]:
        return users[username]
    return None

def generate_TGS_session_key(userload, client):
    ''' 
        - generate TGS_Session_key by hashing db secret key and client name
    '''
    secret_key = client['secret']
    payload = f'{userload}.{secret_key}'
    return hash(payload)
    pass 
    
def init(user_load):
    ''' 
        - user_load is the client_id/username
        - check if requested user is in system 
        - msgA: payload for the TGS
        - msgB: payload for client contianing TGS_Session key
    '''
    users = get_users()
    if users[user_load]:
        client = users[user_load]
        SECRET_KEY = client['secret']

        TGS_session_key = generate_TGS_session_key(user_load, client)
        users[user_load]['TGS_S_K'] = TGS_session_key
        save_users(users)

        rc4 = RC4()
        timeout = 10
        msgA = rc4.encrypt(TGS_session_key, SECRET_KEY)
        msgB = rc4.encrypt(f'{user_load}.{timeout}.{TGS_session_key}', TGS_SECRET_KEY)

        return msgA, msgB
    else:
        return "Error","User Not in System!!"

