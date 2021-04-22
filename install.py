import os, sys
from pathlib import Path

# os.system("sudo apt-get install -y python3-dev libasound2-dev")
os.system("pip3 install -U pip wheel setuptools")
os.system("sudo pip3 install -r requirements.txt")

file = open('{}/.local/share/applications/moein-dns-changer.desktop'.format(Path.home()), 'w+')
cur_path = sys.path[0]
file.write('''[Desktop Entry]
Name= DNS changer
Comment= simple gui linux DNS changer with python3 and PyQt By Moein Aghamirzaei
Exec= gksu python3 {}/main.py
Icon= {}/icon/dns-logo.png
Terminal=false
Type=Application
StartupNotify=true'''.format(cur_path, cur_path))
