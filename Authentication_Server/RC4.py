class RC4(object):
    def array_to_str(self, arr):
        return "".join([str(i) for i in arr])

    def xor(self,m, n):
      return hex(int(m, 16) ^ int(n, 16))[2:].zfill(2)

    def _KSA(self, key):
        S, T = [], []
        for i in range(0, 256):
            S.append(i)
            T.append(ord(key[i % len(key)]))

        j = 0
        for i in range(0, 256):
            j = (j + S[i] + T[i]) % 256
            S[i], S[j] = S[j], S[i]

        return S

    def _PRGA(self, S, length):
        i, j = 0, 0

        key_stream = []
        for i in range(0, length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]

            t = (S[i] + S[j]) % 256

            key_stream.append((hex(S[t])[2:].zfill(2)))

        return key_stream

    def encrypt(self, secret, key):
        cipher = []

        # Get keystream
        p = self._KSA(key)
        keystream = self._PRGA(p, len(secret))

        # Secret to hex
        for s in list(secret):
            cipher.append(hex(ord(s))[2:])

        # Create ciphertext
        for i in range(len(cipher)):
            cipher[i] = self.xor(cipher[i], keystream[i])

        return self.array_to_str(cipher)

    def decrypt(self, cipher, key):
        message = []

        # Split message to hex per 2 character
        s = [cipher[i:i + 2] for i in range(0, len(cipher), 2)]
        
        # Get keystream
        p = self._KSA(key)
        keystream = self._PRGA(p, len(cipher))

        # XOR to get original message from ciphertext
        for i in range(len(s)):
            message.append(self.xor(s[i], keystream[i]))

        hex_message = self.array_to_str(message)

        return bytearray.fromhex(hex_message).decode()


if __name__ == '__main__':
    text = "Test Text"
    key = "Brian"

    enc = RC4()
    cipher = enc.encrypt(text, key)
    message = enc.decrypt(cipher, key)


    print(f'Original Text: {text} \nEncrypted text: {cipher} \nDecrypted Message: {message}')

