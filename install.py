import os
import sys
from pathlib import Path

# os.system("sudo apt-get install -y python3-dev libasound2-dev")
os.system("pip3 install -U pip wheel setuptools")
os.system("sudo pip3 install -r requirements.txt")

cur_path = sys.path[0]

file = open(
    '{}/.local/share/applications/moein-dns-changer.desktop'.format(Path.home()), 'w+')
file.write('''[Desktop Entry]
Name= DNS changer
Comment= simple gui linux DNS changer with python3 and PyQt By Moein Aghamirzaei
Exec= dns_changer
Icon= {}/icon/dns-logo.png
Terminal=false
Type=Application
StartupNotify=true'''.format(cur_path, cur_path))
file.close()

file = open('/usr/bin/dns_changer'.format(Path.home()), 'w+')
file.write('''
#! /bin/bash
exec pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY python3 {}/main.py
'''.format(cur_path))
file.close()
os.system("sudo chmod +x {}/.local/bin/dns_changer".format(Path.home()))

print('------------------\ninstalled successfully')
