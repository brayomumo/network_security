'''
    - Key Distribution Center
'''
from utils.RC4 import RC4
from auth_server import TGS_SECRET_KEY,VALID_P, user_details, hash

def generate_client_server_SK(client_id, server_id):
    ''' Generate a Secret key for client and server '''
    payload = f'{client_id}-TO-{server_id}'
    return hash(payload)


def handle_serviceRequest(msgC, msgD):
    '''
        - msgC is of format [msgB,  service_id]
        - get session_id from msgB after decrypting using TGS_SECRET_KEY
        - use session_id to decrypt msgD
        - compare client_id from msgB to that in msgD
    '''
    rc4 = RC4()
    msgB = msgC[0]
    service_id = msgC[1] # requested service name/id
    serviceB = user_details(service_id) # requested service details 
    if serviceB is not None:
        return "Service Not Found"

    msgB = rc4.decrypt(msgB, TGS_SECRET_KEY)
    msgB_payload = msgB.split(".")

    client_id = msgB_payload[0] # original client_id
    TGS_session_key = msgB_payload[-1] # Original Session Key

    msgD = rc4.decrypt(msgD, TGS_session_key).split('.')
    sender_id = msgD[0] #sender id
    if sender_id == client_id:
        service_SCRTK = serviceB.secret 
        client_server_session_key =  generate_client_server_SK(client_id, service_id)
        msgE = rc4.encrypt(f'{client_id}.{VALID_P}.{client_server_session_key}',service_SCRTK )

        msgF = rc4.encrypt(client_server_session_key, TGS_session_key)
        return msgE, msgF
    else:
        return "Error", "Invalid Details"

    