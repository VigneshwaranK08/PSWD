import argparse
import json

Parser = argparse.ArgumentParser()
SubParser = Parser.add_subparsers()

def addservice(args):
    try:
        with open("Passwords.json",'rb') as jsonfile:
            jsondata = json.load(jsonfile)
    except:
        jsondata = []
    
    jsondata.append({"name":args.name,"field":args.field,"password":args.password})

    with open("Passwords.json",'w') as jsonfile:
        json.dump(jsondata,jsonfile,indent=4)

AddService = SubParser.add_parser("add")
AddService.add_argument("name")
AddService.add_argument('-f','--field')
AddService.add_argument('-p','--password',type=str)
AddService.set_defaults(func=addservice)

args = Parser.parse_args()
args.func(args)