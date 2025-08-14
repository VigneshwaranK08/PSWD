import argparse
import Encryption.Decoding as Decoding
import Encryption.Encoding as Encoding
import json

Parser = argparse.ArgumentParser()
SubParser = Parser.add_subparsers()

def addservice(args):
    try:
        with open("Passwords.json",'rb') as jsonfile:
            jsondata = json.load(jsonfile)
    except:
        jsondata = []
    
    EncryptedPassword = Encoding.Encoder(args.password)

    jsondata.append({"name":args.name,"field":args.field,"password":EncryptedPassword.decode()})

    with open("Passwords.json",'w') as jsonfile:
        json.dump(jsondata,jsonfile,indent=4)

AddService = SubParser.add_parser("add")
AddService.add_argument("name")
AddService.add_argument('-f','--field')
AddService.add_argument('-p','--password',type=str)
AddService.set_defaults(func=addservice)



def listservice(args):

    with open('Passwords.json','rb') as jsonfile:
        jsondata = json.load(jsonfile)

    for dict in jsondata:
        print(dict['name'])
        print(dict['field'])

        DecryptedPassword = Decoding.Decoder(dict['password'])
        print(DecryptedPassword)

ListService = SubParser.add_parser('list')
ListService.add_argument("list",action="store_true")
ListService.set_defaults(func=listservice)


args = Parser.parse_args()
args.func(args)