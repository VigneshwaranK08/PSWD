#!/usr/bin/env python3
import argparse
import Encryption.Decoding as Decoding
import Encryption.Encoding as Encoding
import json
from tabulate import tabulate
from datetime import datetime, timedelta
from types import SimpleNamespace
import os
import platform

if platform.system() == 'Windows':
    path = os.path.expandvars(r'%AppData%/pswd')
elif platform.system() == 'Linux':
    path = os.path.expanduser("~/.local/share/pswd")
else:
    path = None
    
try:
    os.mkdir(f"{path}")
except FileExistsError:
    pass

Parser = argparse.ArgumentParser(prog="PSWD : Password Manager",
                                 description="Manage All your passwords with ease and protection",
                                 epilog="Don't worry, your passwords are safe :). Thank You !")
SubParser = Parser.add_subparsers(help="All the avaiable Sub-Commands")

def CheckMasterStatus():
    
    try:
        with open(f'{path}/Status.json','r') as jsonfile:
            MasterUnlockStatus = json.load(jsonfile)['MasterUnlockStatus']
    
    except:
        with open(f'{path}/Status.json','w') as jsonfile:
            json.dump({"MasterUnlockStatus": False},jsonfile,indent=4)
        MasterUnlockStatus = False
        
    return MasterUnlockStatus

def addservice(args):

    if not CheckMasterStatus():
        ForceUnlockTrue = SimpleNamespace(unlock = True)
        unlock(ForceUnlockTrue)
    
    with open(f'{path}/Status.json','r') as jsonfile:
        data = json.load(jsonfile)

    if CheckMasterStatus() and (datetime.now() - datetime.fromisoformat(data["LastAct"])) < timedelta(minutes=3):
        try:
            with open(f"{path}/Passwords.json",'rb') as jsonfile:
                jsondata = json.load(jsonfile)
        except:
            jsondata = []
        
        EncryptedPassword = Encoding.Encoder(args.password)

        jsondata.append({"name":args.name,"field":args.field,"password":EncryptedPassword.decode()})

        with open(f"{path}/Passwords.json",'w') as jsonfile:
            json.dump(jsondata,jsonfile,indent=4)
        
        print("Password Successfully saved")

        with open(f'{path}/Status.json','w') as jsonfile:
            data["LastAct"] = datetime.now().isoformat()
            json.dump(data,jsonfile,indent=4)
    
    else:
        with open(f'{path}/Status.json','r') as jsonfile:
            data = json.load(jsonfile)

        with open(f'{path}/Status.json','w') as jsonfile:
            data["MasterUnlockStatus"] = False
            json.dump(data,jsonfile,indent=4)
        
        print("Session Expired !")
        print("To unlock Usage : pswd unlock")


AddService = SubParser.add_parser("add",help="Enter the name of the service for the password")
AddService.add_argument("name")
AddService.add_argument('-f','--field',help="Enter any other field for the service")
AddService.add_argument('-p','--password',type=str,help="Enter the password")
AddService.set_defaults(func=addservice)



def listservice(args):

    if not CheckMasterStatus():
        ForceUnlockTrue = SimpleNamespace(unlock = True)
        unlock(ForceUnlockTrue)

    with open(f'{path}/Status.json','r') as jsonfile:
        data = json.load(jsonfile)

    if CheckMasterStatus() and (datetime.now() - datetime.fromisoformat(data["LastAct"])) < timedelta(minutes=3):
        with open(f'{path}/Passwords.json','rb') as jsonfile:
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

        with open(f'{path}/Status.json','w') as jsonfile:
            data["LastAct"] = datetime.now().isoformat()
            json.dump(data,jsonfile,indent=4)
    
    else:
        with open(f'{path}/Status.json','r') as jsonfile:
            data = json.load(jsonfile)

        with open(f'{path}/Status.json','w') as jsonfile:
            data["MasterUnlockStatus"] = False
            json.dump(data,jsonfile,indent=4)
        
        print("Session Expired !")
        print("To unlock Usage : pswd unlock")

ListService = SubParser.add_parser('list',help="View all your passwords")
ListService.add_argument("list",action="store_true",help="View all the information")
ListService.set_defaults(func=listservice)


def unlock(args):
    if args.unlock:
        with open(f'{path}/Status.json','rb') as jsonfile:
            data = json.load(jsonfile)

        if len(data) == 1:
            MasterPassword = input("Set New Master Password : ")

            with open(f'{path}/Status.json','w') as jsonfile:
                data["MasterUnlockStatus"] = True
                data["MasterPassword"] = MasterPassword
                data["LastAct"] = datetime.now().isoformat()
                json.dump(data,jsonfile,indent=4)
        
        else:
            Input = input("Enter Master password : ")

            if data["MasterPassword"] == Input:

                with open(f'{path}/Status.json','r') as jsonfile:
                    data = json.load(jsonfile)
                    data["MasterUnlockStatus"] = True

                with open(f'{path}/Status.json','w') as jsonfile:
                    data["LastAct"] = datetime.now().isoformat()
                    json.dump(data,jsonfile,indent=4)
                
                print("Unlocked Successfully")
            
    else:
        return

Unlock = SubParser.add_parser('unlock',help="Enter or Create your Master Password ")
Unlock.add_argument('unlock',action='store_true',help="If Session expired, Enter your master password to renew your session")
Unlock.set_defaults(func=unlock)



def reset(args):
    confirm = input("Reset will cause all the existing data to be deleted permanently (y/n) : ")
    if confirm == 'y':
        os.remove(f'{path}/Status.json')
        os.remove(f'{path}/Passwords.json')
        print('Data Deleted')
    else:
        print('Data not Deleted')

Reset = SubParser.add_parser('reset',help="Clear all your passwords")
Reset.add_argument('reset',nargs='*',help="Clear all the passwords")
Reset.set_defaults(func=reset)


def getservice(args):

    if not CheckMasterStatus():
        ForceUnlockTrue = SimpleNamespace(unlock = True)
        unlock(ForceUnlockTrue)

    with open(f'{path}/Status.json','r') as jsonfile:
        data = json.load(jsonfile)

    if CheckMasterStatus() and (datetime.now() - datetime.fromisoformat(data["LastAct"])) < timedelta(minutes=3):
        
        ServiceName = args.name[0]
        try:
            with open(f'{path}/Passwords.json','r') as jsonfile:
                data = json.load(jsonfile)

            res = []
            for dict in data:
                if dict['name'] == ServiceName:
                    temp = {}
                    temp['Name'] = dict['name']
                    temp['Field'] = dict['field']
                    temp['Password'] = Decoding.Decoder(dict['password'])
                    res.append(temp)
            
            print(tabulate(res,headers="keys",tablefmt='github'))   
            
        except:
            return "File Doesnt exist , Enter a password first"
        
        with open(f'{path}/Status.json','r') as jsonfile:
            sdata = json.load(jsonfile)

        with open(f'{path}/Status.json','w') as jsonfile:
            sdata["LastAct"] = datetime.now().isoformat()
            json.dump(sdata,jsonfile,indent=4)

    else:
        with open(f'{path}/Status.json','r') as jsonfile:
            data = json.load(jsonfile)

        with open(f'{path}/Status.json','w') as jsonfile:
            data["MasterUnlockStatus"] = False
            json.dump(data,jsonfile,indent=4)
        
        print("Session Expired !")
        print("To unlock Usage : pswd unlock")

Get = SubParser.add_parser('get',help="Get the password for the specified Service name")
Get.add_argument('name',nargs=1,help="Enter the name of the service and get the passwords")
Get.set_defaults(func=getservice)

args = Parser.parse_args()
args.func(args)