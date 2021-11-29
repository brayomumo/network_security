from utils.RC4 import RC4
from datetime import datetime
from hashlib import md5

USERNAME = ''
SESSION_KEY = ''
def get_details():
    USERNAME = input("Enter username: (Alice or Bob): ")
    password = input(f"Enter password for {USERNAME}: ")

    SECRET_KEY = md5(password.encode("ascii", 'ignore'))

    return  SECRET_KEY


def get_TGS_SESSION_KEY(msgA, secret_key):
    ''' 
        - This decrypts message A from Authentication Server
        - It returns the client_TGS session key required to communicate with  TGS
    '''
    rc4 = RC4()
    session_key = rc4.decrypt(msgA, secret_key)

    return session_key


def request_service(msgB, TGS_session_key):
    service_id = input("Enter name of user to communicate to: ").lower()
    rc4 = RC4()
    msgC = [msgB, service_id]

    client_id = USERNAME
    timestamp = 'now'
    msgD = rc4.encrypt(f'{client_id}.{timestamp}', TGS_session_key) # client_id.timestamp

    return msgC, msgD
    

def handle_serviceRequestReply( msgF, TGS_session_key):
    '''
        - decrypt msgF
        - set session_key
    '''
    rc4 = RC4()
    SESSION_KEY = rc4.decrypt(msgF, TGS_session_key)

    return SESSION_KEY


def conduct_service(msgE):
    ''' 
        - generate message to be send to the other service for authentication
    '''
    timestamp = "now"
    authenticator = f'{USERNAME}.{timestamp}'
    rc4 = RC4()
    msgG = rc4.encrypt(authenticator, SESSION_KEY)

    return msgE, msgG

def authenticate_service(msgE, msgG):
    secret_key = get_details()
    rc4 = RC4()
    payload = rc4.decrypt(msgE, secret_key).split('.')
    validity = payload[1]
    now = datetime.now()
    if validity > now:
        SESSION_KEY = payload[-1]
        sender_id = payload[0]

        payloadG = rc4.decrypt(msgG, SESSION_KEY).split('.')
        client_id = payloadG[0]
        initial_client = payload[0]

        if client_id == initial_client:
            return "Authenticated"
        else:
            return "Authentication Failed"

if __name__ == '__main__':
    while True:
        choice = input("choose an Option (1 or 2):\n 1: Initiate Communication\n 2: Accept communication \n exit: Quit\n")
        if int(choice) == 1:
            secret_key = get_details()

            auth_reply = input("Enter Authentication Server Reply: ").split(":")
            print(f'secret key: {secret_key}')
            msgA = auth_reply[0]
            msgB = auth_reply[1]

            TGS_Session_key = get_TGS_SESSION_KEY(msgA, secret_key)
            print(f'TGS session key is: {TGS_Session_key}')

            msgC, msgD = request_service(msgB, TGS_Session_key)
            print("Service Request Payload: {msgC}:{msgD}")

            service_response = input("Enter TGT Server Reply: ").split(":")
            msgE = service_response[0]
            msgF = service_response[1]

            session_key = handle_serviceRequestReply(msgF, TGS_Session_key)

            msgE, msgG = conduct_service(msgE)
            print("Peer Payload: {msgE}:{msgG}")

        elif int(choice) == 2:
            payload = input("Enter Peer payload: ").split(":")

            status = authenticate_service(payload[0], payload[1])
            print(f"Authentication status: {status}")
        else:
            break


