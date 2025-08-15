from cryptography.fernet import Fernet
import os

def abspath(filename):
    filepath = os.path.dirname(__file__) # this return the abs path of this file i.e /home/vignesh/Documents/roadmap-sh/python/PasswordManager/Encryption
    
    return os.path.join(filepath,filename) # its like join the above path / filename , but make sure its cross-platform

def Encoder(password):
    with open(abspath('key.key'),'rb') as keyfile:
        key = keyfile.read()
        key = Fernet(key) # byte object Fernet object

    EncryptedPassword = key.encrypt(password.encode())

    return EncryptedPassword