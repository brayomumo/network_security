from hashlib import md5
from asymmetric import generate_keys, encrypt, decrypt

def hash_data(data):
    ''' hash data using md5'''
    e_data = data.encode('ascii', 'ignore')
    data_hash = md5(e_data)
    return data, data_hash.hexdigest()

   
def certificate(data, priv_key):
    '''
        - hash data 
        - encrypt data using private key
        - return certificate in format cipher.hash
    '''
    data,hash = hash_data(data)
    cipher = encrypt(data, priv_key)
    final = []
    for i in cipher:
        final.append("-".join(str(x)for x in i))
    cipher = " ".join(final)
    return f'{cipher}.{hash}'
    
def decrypt_certificate(cert, pub_key):
    ''' 
        - Decrypts using the sender's publick key
        - returns data.hash
    '''
    certificate = cert.split('.')
    data_cipher = certificate[0]
    cipher =  data_cipher.split()
    data_cipher = [i.split("-") for i in cipher]
    text = decrypt(data_cipher, pub_key)
    return [text, certificate[1]]



def check_certificate(cert, pub_key):
    '''
        - decrypts the certificate to get data 
        - hashes decrypted data 
        - check hash of decrypted data is the same as hash in certificate
    '''
    data_hash = decrypt_certificate(cert, pub_key)
    data = data_hash[0]
    data, hash = hash_data(data)
    if hash == data_hash[1]: return "valid"
    return "invalid"


if __name__ == '__main__':
    pub, prv = generate_keys()

    # generate certificate 
    cipher = certificate("generating new certificate for new users",prv)
    print(f'Certificate: {cipher}')

    # check validity of recieved certificate
    validity = check_certificate(cipher, pub)
    print(f'Certificate is {validity}')
