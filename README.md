# GUI-DNS-changer-for-linux
simple GUI DNS changer for linux with PyQt5

tested with linux "mint and ubuntu"

### Installation
```
git clone https://github.com/mrmoein/GUI-DNS-changer-for-linux.git
cd GUI-DNS-changer-for-linux/
pip3 install PyQt5
sudo apt-get install python3-pyqt5
sudo python3 dns.py
```

### Screenshots
![](https://uupload.ir/files/ats0_screenshot-1.png)
![](https://uupload.ir/files/cnn4_screenshot-2.png)

### How add launcher for linux
add `DNS-Changer.desktop` to your `~/.local/share/applications` directory and paste this into it
```
[Desktop Entry]
Name=DNS Changer
Exec=pkexec python3 /home/moein/Programming/Python/GUI-DNS-changer-for-linux/dns.py
Comment=
Terminal=false
Icon=/home/moein/Programming/Python/GUI-DNS-changer-for-linux/dns-logo.png
Type=Application
```