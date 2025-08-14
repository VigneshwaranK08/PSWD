import argparse

Parser = argparse.ArgumentParser()
SubParser = Parser.add_subparsers()

def addservice(args):
    print("added password",args)

AddService = SubParser.add_parser("add")
AddService.add_argument("name")
AddService.add_argument('-f','--field')
AddService.add_argument('-p','--password',nargs=1)
AddService.set_defaults(func=addservice)

args = Parser.parse_args()
args.func(args)