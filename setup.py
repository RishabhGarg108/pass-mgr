import sys, os
import argparse
from password_generator import generateRandomPassword


parser = argparse.ArgumentParser()
parser.add_argument("root_password", help="Sets the root password for the app.")
parser.add_argument("-s", "--security_key", help="Sets the security key for encryption.")
parser.add_argument("-a", "--auth_type", type=int, help="Sets the authentication type.")
args = parser.parse_args()

env = open('.env', 'w')

env.write(f'ROOT_PASSWORD={args.root_password}\n')

if args.security_key:
  env.write(f'SECURITY_KEY={args.security_key}\n')
else:
  security_key = generateRandomPassword()
  env.write(f'SECURITY_KEY={security_key}\n')

if args.auth_type:
  env.write(f'AUTHENTICATION_TYPE={args.auth_type}\n')
else:
  env.write(f'AUTHENTICATION_TYPE={1}\n')
