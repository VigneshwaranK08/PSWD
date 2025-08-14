from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open('key.key','wb') as keyfile:
    keyfile.write(key)