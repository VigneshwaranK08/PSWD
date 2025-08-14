from cryptography.fernet import Fernet
import os

def abspath(filename):
    folderpath = os.path.dirname(__file__)
    path = os.path.join(folderpath,filename)

    return path

def Decoder(password):

    with open(abspath('key.key'),'rb') as keyfile:
        key = keyfile.read()
        key = Fernet(key) # str to byte

    DecryptedPassword = key.decrypt(password).decode()

    return DecryptedPassword
