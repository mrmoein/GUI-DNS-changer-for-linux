import os, sys
from pathlib import Path

file_path = '{}/.local/share/applications/moein-dns-changer.desktop'.format(Path.home())

if os.path.exists(file_path):
    os.remove(file_path)
    print('Desktop Entry removed')
else:
    print('Desktop Entry not found!')
