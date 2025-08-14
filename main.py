import argparse

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

def addservice(args):
    print("added password",args)

addservice = subparser.add_parser("add")
addservice.add_argument("name")
addservice.add_argument('-f','--field')
addservice.add_argument('-p','--password',nargs=1)
addservice.set_defaults(func=addservice)

args = parser.parse_args()
args.func(args)