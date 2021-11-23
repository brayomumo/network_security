'''
     - generate private-public keys
     - share pub keys
     - sign a document
     - share document
     - proof document is signed
'''
import random


def prime_nums(n):
    nums = [i for i in range(2, n+1)]
    for i in nums:
        p = i
        for j in range(i, n//2):
            prod = p * j
            if prod > n:
                break
            else:
                try:
                    nums.remove(prod)
                except:
                    continue

    return nums


def __gcd(a, b):
    if a == 0 or b == 0: return 0

    if a == b: return a

    if a > b: return __gcd(a-b, b)

    return __gcd(a, b-a)


def get_d(Qn, e):
    '''
     - given Qn and e, it finds a unique number d where e*d mod Qn =1
    '''
    d = 0
    for i in range(2, Qn):
        d = (i * e) % Qn
        if d == 1:
            d = i
            break
    return d


def get_e(Qn):
    while(True):
        e = random.randint(2, Qn)
        if __gcd(e, Qn) == 1:
            return e
    

def generate_keys():
    primes = prime_nums(100)
    p_q = random.choices(primes, k=2)
    p, q = p_q[0], p_q[1]

    n = p * q
    Qn = (p-1) * (q-1)

    e = get_e(Qn)
    pub_key = [e, n]

    d = get_d(Qn, e)
    pr_key = [d,n]

    if d == e:
        return generate_keys()

    return pub_key, pr_key

    

def encrypt(message, pub_key):
    message = message.split()
    cipher = list()
    for word in message:
        cip = list()
        for i in word:
            if not i.isdigit():
                i = ord(i)
            c = (i**pub_key[0])%pub_key[1]
            cip.append(c)
        cipher.append(cip)
    return cipher

def decrypt(cipher, pr_key):
    message = list()
    for word in cipher:
        cip = list()
        for i in word:
            text = chr((int(i)**pr_key[0]) % pr_key[1])
            cip.append(text)
        message.append("".join(cip))
        
    return " ".join(message)
        

    
# if __name__ == '__main__':
#     keys = generate_keys()
#     public = keys[0]
#     private = keys[1]

#     data  = input("Enter data to encrypt: ")
#     cipher = encrypt(data, public)
#     print(f"\ncipher is: {cipher}")

#     text = decrypt(cipher, private)

#     print(f"\nDecrypted text: {text}")