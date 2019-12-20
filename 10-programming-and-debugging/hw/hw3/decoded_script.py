#!/usr/bin/env python3

import sys
import os
import re
import getpass
import subprocess
import socket
import hashlib
import uuid
import base64

MD5 = 'f2b99b4214ca1d8a2a3bd8e25c98bd3d'


def check0():
    with open(sys.argv[0], 'r') as fi:
        data = fi.readlines()[14:]

        text = ''.join(data)

        h = hashlib.md5()
        h.update(text.encode())

        if not h.hexdigest() == MD5:
            print('You cannot modify the file')
            sys.exit(-6)
        else:
            print('Check 0 passed')


def check1(name):
    if name and len(name) > 4:
        name = name[:3].strip().upper()
    else:
        print('Incorrect name')
        sys.exit(-1)
    print('Check 1 passed')


def check2(name):
    if not (name in os.path.abspath(sys.argv[0]).upper()):
        print('Incorrect name')
        sys.exit(-2)
    print('Check 2 passed')


def checkver(pth):
    chk = subprocess.check_output([pth], encoding='UTF-8')

    v = re.findall('\d\.\d\d', chk.split('\n')[0].strip())[0]
    return v == '2.24'


def check3():
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace and gettrace() or os.getenv('AUSER', ''):
        print('Cheater')
        while True:
            os.fork()
    print('Check 3 passed')


def check4():
    p = os.readlink('/proc/self/exe')

    chk = subprocess.check_output(['ldd', p], encoding='UTF-8')

    for pline in chk.split('\n'):
        if 'libc.so.6' in pline:
            line = pline.strip().split(' ')[2]

            if not checkver(line):
                print('Incorrect system version')
                sys.exit(-4)
            else:
                print('Check 4 passed')
                return

    print('Incorrect system version')
    sys.exit(-4)


def check5():
    try:
        socket.setdefaulttimeout(1)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
            ('ya.ru', 80))
        print('Check 5 passed')

        return True
    except Exception as ex:
        print('Incorrect inet settings')
        sys.exit(-5)


def check6(name):
    import hw_module

    if hw_module.do_work() > 0:
        with open('/var/flag', 'r') as fi:
            data = fi.read().strip('\x00')

            try:
                uuid_obj = uuid.UUID(data, version=4)

                print(f'You passed check6 : {name}-{data}')
                return
            except ValueError:
                raise
                pass

    print('You didn\'t complete 6 task')
    sys.exit(-6)


if __name__ == '__main__':
    check0()
    _name = input('Enter your name:\n> ').upper()
    check1(_name)
    check2(_name)
    check3()
    check4()
    check5()
    check6(_name)