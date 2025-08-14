from cryptography.fernet import Fernet

def Encoder(password):
    with open('/home/vignesh/Documents/roadmap-sh/python/PasswordManager/Encryption/key.key','rb') as keyfile:
        key = keyfile.read()
        key = Fernet(key)

    EncryptedPassword = key.encrypt(password.encode())

    return EncryptedPassword