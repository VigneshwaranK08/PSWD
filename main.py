import argparse
import Encryption.Decoding as Decoding
import Encryption.Encoding as Encoding
import json
from tabulate import tabulate
from datetime import datetime, timedelta
from types import SimpleNamespace
import os

Parser = argparse.ArgumentParser()
SubParser = Parser.add_subparsers()

def CheckMasterStatus():
    
    try:
        with open('Status.json','r') as jsonfile:
            MasterUnlockStatus = json.load(jsonfile)['MasterUnlockStatus']
    
    except:
        with open('Status.json','w') as jsonfile:
            json.dump({"MasterUnlockStatus": False},jsonfile,indent=4)
        MasterUnlockStatus = False
        
    return MasterUnlockStatus

def addservice(args):

    if not CheckMasterStatus():
        ForceUnlockTrue = SimpleNamespace(unlock = True)
        unlock(ForceUnlockTrue)
    
    with open('Status.json','r') as jsonfile:
        data = json.load(jsonfile)

    if CheckMasterStatus() and (datetime.now() - datetime.fromisoformat(data["LastAct"])) < timedelta(minutes=3):
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

        with open('Status.json','w') as jsonfile:
            data["LastAct"] = datetime.now().isoformat()
            json.dump(data,jsonfile,indent=4)
    
    else:
        with open('Status.json','r') as jsonfile:
            data = json.load(jsonfile)

        with open('Status.json','w') as jsonfile:
            data["MasterUnlockStatus"] = False
            json.dump(data,jsonfile,indent=4)
        
        print("Session Expired !")
        print("To unlock Usage : pswd unlock")


AddService = SubParser.add_parser("add")
AddService.add_argument("name")
AddService.add_argument('-f','--field')
AddService.add_argument('-p','--password',type=str)
AddService.set_defaults(func=addservice)



def listservice(args):

    if not CheckMasterStatus():
        ForceUnlockTrue = SimpleNamespace(unlock = True)
        unlock(ForceUnlockTrue)

    with open('Status.json','r') as jsonfile:
        data = json.load(jsonfile)

    if CheckMasterStatus() and (datetime.now() - datetime.fromisoformat(data["LastAct"])) < timedelta(minutes=3):
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

        with open('Status.json','w') as jsonfile:
            data["LastAct"] = datetime.now().isoformat()
            json.dump(data,jsonfile,indent=4)
    
    else:
        with open('Status.json','r') as jsonfile:
            data = json.load(jsonfile)

        with open('Status.json','w') as jsonfile:
            data["MasterUnlockStatus"] = False
            json.dump(data,jsonfile,indent=4)
        
        print("Session Expired !")
        print("To unlock Usage : pswd unlock")

ListService = SubParser.add_parser('list')
ListService.add_argument("list",action="store_true")
ListService.set_defaults(func=listservice)


def unlock(args):
    if args.unlock:
        with open('Status.json','rb') as jsonfile:
            data = json.load(jsonfile)

        if len(data) == 1:
            MasterPassword = input("Set New Master Password : ")

            with open('Status.json','w') as jsonfile:
                data["MasterUnlockStatus"] = True
                data["MasterPassword"] = MasterPassword
                data["LastAct"] = datetime.now().isoformat()
                json.dump(data,jsonfile,indent=4)
        
        else:
            Input = input("Enter Master password : ")

            if data["MasterPassword"] == Input:

                with open('Status.json','r') as jsonfile:
                    data = json.load(jsonfile)
                    data["MasterUnlockStatus"] = True

                with open('Status.json','w') as jsonfile:
                    data["LastAct"] = datetime.now().isoformat()
                    json.dump(data,jsonfile,indent=4)
                
                print("Unlocked Successfully")
            
    else:
        return

Unlock = SubParser.add_parser('unlock')
Unlock.add_argument('unlock',action='store_true')
Unlock.set_defaults(func=unlock)



def reset(args):
    confirm = input("Reset will cause all the existing data to be deleted permanently (y/n) : ")
    if confirm == 'y':
        os.remove('Status.json')
        os.remove('Passwords.json')
        print('Data Deleted')
    else:
        print('Data not Deleted')

Reset = SubParser.add_parser('reset')
Reset.add_argument('reset',nargs='*')
Reset.set_defaults(func=reset)


def get(args):
    if not CheckMasterStatus():
        ForcedTrue = SimpleNamespace(unlock=True)
        unlock(ForcedTrue)

    with open('Status.json','r') as jsonfile:
        data = json.load(jsonfile)

    if CheckMasterStatus() and ( datetime.now() - datetime.fromisoformat(data['LastAct']) ) < timedelta(minutes=3):
        
        ServiceName = args.name
        try:
            with open('Passwords.json','r') as jsonfile:
                data = json.load(jsonfile)
            res = []
            for dict in data:
                if dict['name'] == ServiceName:
                    temp = {}
                    temp['Name'] = dict['name']
                    temp['Field'] = dict['field']
                    temp['Password'] = Decoding.Decoder(dict['password'])
                    res.append(temp)
            
            print(tabulate(res,headers='keys',tablefmt='github'))
            
        except:
            return "File Doesnt exist , Enter a password first"
        
        with open('Status.json','w') as jsonfile:
            data["LastAct"] = datetime.now().isoformat()
            json.dump(data,jsonfile,indent=4)

    else:
        with open('Status.json','r') as jsonfile:
            data = json.load(jsonfile)

        with open('Status.json','w') as jsonfile:
            data["MasterUnlockStatus"] = False
            json.dump(data,jsonfile,indent=4)
        
        print("Session Expired !")
        print("To unlock Usage : pswd unlock")

Get = SubParser.add_parser('get')
Get.add_argument('name',nargs=1)
Get.set_defaults(func=get)

args = Parser.parse_args()
args.func(args)