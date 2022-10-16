"""
    Please implement a variant of Vigenère cipher (20 points):
        a. Key length can be from 1-3
        b. Each character in the key must be upper case letters (i.e., ‘A’-‘Z’)
        c. Each character in the cipher text can be any character from the ASCII table
"""

def generateKey(string, key):
    key = list(key)
    if len(string) == len(key):
        return key

    for i in range(len(string) - len(key)):
        key.append(key[i%len(key)])

    return ("".join(key))

def encrypt(string, key):
    cipher_text = []

    for i in range(len(string)):
        x = (ord(string[i]) + ord(key[i])) % 26
        x += ord('A')

        cipher_text.append(chr(x))

    return "".join(cipher_text)

def decrypt(cipher_text, key):
    orig_text = []
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
        x += ord('A')
        orig_text.append(chr(x))

    return "".join(orig_text)

if __name__ == "__main__":
    string = str(input("string:"))
    key = str(input("key:"))

    genKey = generateKey(string, key)
    cipher_text = encrypt(string, genKey)
    print("Encrypted string: ", cipher_text)

    print("Decrypted string:" , decrypt(cipher_text, genKey))