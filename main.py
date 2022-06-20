import hashlib
import json
import os
import sys
import getpass
import random

if not os.path.exists('passwords.json'):
    i = input('passwords.json file does not exist. Create file?(y/n):')
    if i == 'y':
        print('passwords.json file created')
        with open('passwords.json', 'w') as f:
            f.write('{}')
    else:
        print('File not created. Ending program. ')
        sys.exit()

with open('passwords.json', 'r') as f:
    passwords = json.loads(f.read())


def PasswordTransform(passwd, rules=None):
    if rules is None:
        rules = []
    passwd = passwd.replace(passwd[0], '')  # Delete all instances of the first character
    new = ''
    for i, ii in enumerate(passwd):  # get the next pair of digits
        if i == len(passwd) - 1:
            break
        if i % 2 == 0:
            if chr(int(ii + passwd[i + 1], 16) % 91 + 33) not in rules:
                new += chr(int(ii + passwd[i + 1], 16) % 91 + 33)
            else:
                new += str(ii + passwd[i + 1])
    return new


if len(sys.argv) != 2:
    print('Please include 1 command. ')
    sys.exit()

command = sys.argv[1]

if command == 'list':
    if len(passwords) == 0:
        print('No passwords stored')
    else:
        print('Passwords:')
        for i in passwords:
            print(f'{i}:  Encoding:{passwords[i][1]}')
elif command == 'add':
    name = input('Password name:')
    if name in passwords:
        print('Password already exists. ')
        sys.exit()
    MainPassword = getpass.getpass('Main password:')
    if getpass.getpass('Please repeat password:') != MainPassword:
        print('Passwords do not match. ')
        sys.exit()
    salt = ''
    for i in range(100):
        salt = salt + random.choice([chr(ii) for ii in range(33, 123)])
    algorithm = input('Hashing algorithm (sha256 sha384 sha512):')  # sha256
    if algorithm == 'sha256':
        password = str(hashlib.sha256((MainPassword + name + salt).encode()).hexdigest())
    elif algorithm == 'sha384':
        password = str(hashlib.sha384((MainPassword + name + salt).encode()).hexdigest())
    elif algorithm == 'sha512':
        password = str(hashlib.sha512((MainPassword + name + salt).encode()).hexdigest())
    else:
        print('Please only use sha256, sha384, or sha512. ')
        sys.exit()
    if input('Exclude characters from the password?(y/N):') == 'y':
        exclude = input(
            'List all of the characters you don\'t want to be in your password, separated by commas:').split(',')
    else:
        exclude = []
    print(f'Your password is: {PasswordTransform(password, exclude)}')
    passwords[name] = [salt, algorithm, exclude]
    with open('passwords.json', 'w') as f:
        f.write(json.dumps(passwords))
elif command == 'help':
    print('This is a program for storing  and generating passwords. ')
    print('Usage: python3 main.py <command>')
    print('Commands:')
    print('    list: list all of the passwords in file')
    print('    add: add a password to the file')
    print('    help: display a list of commands')
    print('    remove: remove a password from the file')
    print('    decrypt: decrypt a password in the file')  # do
elif command == 'remove':
    password = input('Password to remove:')
    if password in passwords:
        del passwords[password]
    else:
        print('That password is not in the file. ')
        sys.exit()
    with open('passwords.json', 'w') as f:
        f.write(json.dumps(passwords))
elif command == 'decrypt':
    name = input('Password name:')
    if name not in passwords:
        print('Password does not exist')
        sys.exit()
    MainPassword = getpass.getpass('Main password:')
    if getpass.getpass('Please repeat password:') != MainPassword:
        print('Passwords do not match. ')
        sys.exit()
    salt, algorithm, exclude = passwords[name]
    if algorithm == 'sha256':
        password = str(hashlib.sha256((MainPassword + name + salt).encode()).hexdigest())
    elif algorithm == 'sha384':
        password = str(hashlib.sha384((MainPassword + name + salt).encode()).hexdigest())
    elif algorithm == 'sha512':
        password = str(hashlib.sha512((MainPassword + name + salt).encode()).hexdigest())
    else:
        raise ValueError
    print(f'Your password is: {PasswordTransform(password, exclude)}')
