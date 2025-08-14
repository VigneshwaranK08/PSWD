from cryptography.fernet import Fernet

def Encoder(password):
    with open('key.key','rb') as keyfile:
        key = keyfile.read()
        key = Fernet(key)

    EncryptedPassword = key.encrypt(password.encode())

    return EncryptedPassword