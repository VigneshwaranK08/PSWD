import argparse
import Encryption.Decoding as Decoding
import Encryption.Encoding as Encoding
import json
from tabulate import tabulate
from datetime import datetime, timedelta
from types import SimpleNamespace

Parser = argparse.ArgumentParser()
SubParser = Parser.add_subparsers()

def CheckMasterStatus():
    
    try:
        with open('Status.json','rb') as jsonfile:
            MasterUnlockStatus = json.load(jsonfile)['MasterUnlockStatus']
    
    except:
        with open('Status.json','wb') as jsonfile:
            json.dump({"MasterUnlockStatus": False},jsonfile,indent=4)
        MasterUnlockStatus = False
        
    return MasterUnlockStatus

def addservice(args):

    if not CheckMasterStatus():
        args = SimpleNamespace(unlock = True)
        unlock(args)
    
    try:
        with open("Passwords.json",'rb') as jsonfile:
            jsondata = json.load(jsonfile)
    except:
        jsondata = []
    
    EncryptedPassword = Encoding.Encoder(args.password)

    jsondata.append({"name":args.name,"field":args.field,"password":EncryptedPassword.decode()})

    with open("Passwords.json",'w') as jsonfile:
        json.dump(jsondata,jsonfile,indent=4)
    
    print("Password Successfully saved")

AddService = SubParser.add_parser("add")
AddService.add_argument("name")
AddService.add_argument('-f','--field')
AddService.add_argument('-p','--password',type=str)
AddService.set_defaults(func=addservice)



def listservice(args):

    if not CheckMasterStatus():
        args = SimpleNamespace(unlock = True)
        unlock(args)

    with open('Passwords.json','rb') as jsonfile:
        jsondata = json.load(jsonfile)

    PasswordList = []

    for dict in jsondata:
        temp = {}
        temp["Name"] = dict['name']
        temp["Field"] = dict['field']
        DecryptedPassword = Decoding.Decoder(dict['password'])
        temp["Password"] = DecryptedPassword

        PasswordList.append(temp)

    print(tabulate(PasswordList,headers="keys",tablefmt='github'))

ListService = SubParser.add_parser('list')
ListService.add_argument("list",action="store_true")
ListService.set_defaults(func=listservice)


def unlock(args):
    if args.unlock:
        with open('Status.json','rb') as jsonfile:
            data = json.load(jsonfile)

        if len(data) == 1:
            MasterPassword = input("Set Master Password : ")

            with open('Status.json','wb') as jsonfile:
                data["MasterUnlockStatus"] = True
                data["MasterPassword"] = MasterPassword
                json.dump(data,jsonfile,indent=4)
        
        else:
            Input = input("Enter Master password : ")

            if data["MasterPassword"] == Input:

                with open('Status.json','rb') as jsonfile:
                    data = json.load(jsonfile)
                    data["MasterUnlockStatus"] = True

                with open('Status.json','wb') as jsonfile:
                    json.dump(data,jsonfile,indent=4)
            
    else:
        return

Unlock = SubParser.add_parser('unlock')
Unlock.add_argument('unlock',action='store_true')
Unlock.set_defaults(func=unlock)

args = Parser.parse_args()
args.func(args)