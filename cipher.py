##################################################
#                                                #
#   Paul Brian Mumo - P15/128559/2018            #
#                                                #
##################################################


def encrypt(message, key):
    '''
        For every character in the message, it is replaced by a character key-times away in the ASCII code
        (Ex. 'a' = 97 with  key=1 becomes 'b'=98)
    '''
    cipher = list()
    for m in message:
        cipher_char = ord(m) + key
        cipher.append(chr(cipher_char))
    return "".join(cipher)


def decrypt(cipher, key):
    '''
        For every character in the message, it is replaced by a character key-times before it in the ASCII code
        (Ex. 'b' = 98 with  key=1 becomes 'a'=97)
    '''
    message = list()
    for c in cipher:
        msg_letter = ord(c) - key
        message.append(chr(msg_letter))
    return "".join(message)

def get_key_from_user():
    '''
        - Secret key should be a number
        - Secret key function makes sure key is less than 26 
    '''
    key = input("Enter Secret Key\n\t(Must be a number): ")
    if key.isdigit():
        key = int(key)
        if key >= 26:
            key = int(key)%26
        return key 
    else:
        return get_key_from_user()


if __name__ == '__main__':
    key = get_key_from_user()
    Message = input("Enter message: ")

    cipher = encrypt(Message, key)
    print(f"------------------\nCipher is:\t{cipher}")

    message = decrypt(cipher, key)
    print(f"------------------\nMessage after Decrypting is:\t{message}\n------------------")