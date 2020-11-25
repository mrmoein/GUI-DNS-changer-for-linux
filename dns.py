import collections
import json
import os
import sys
import subprocess
from ipaddress import ip_address, IPv4Address
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.index = 0

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(359, 332)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dns_list_box = QtWidgets.QComboBox(self.centralwidget)
        self.dns_list_box.setGeometry(QtCore.QRect(10, 20, 341, 27))
        self.dns_list_box.setObjectName("dns_list_box")
        self.dns_list_box.addItem("")
        for dnsName in dnsList:
            self.dns_list_box.addItem("")
        self.name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.name_input.setGeometry(QtCore.QRect(110, 70, 241, 27))
        self.name_input.setObjectName("name_input")
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(10, 70, 79, 21))
        self.name_label.setObjectName("name_label")
        self.primary_input = QtWidgets.QLineEdit(self.centralwidget)
        self.primary_input.setGeometry(QtCore.QRect(110, 110, 241, 27))
        self.primary_input.setText("")
        self.primary_input.setObjectName("primary_input")
        self.primary_label = QtWidgets.QLabel(self.centralwidget)
        self.primary_label.setGeometry(QtCore.QRect(10, 110, 91, 21))
        self.primary_label.setObjectName("primary_label")
        self.secondary_input = QtWidgets.QLineEdit(self.centralwidget)
        self.secondary_input.setGeometry(QtCore.QRect(110, 150, 241, 27))
        self.secondary_input.setObjectName("secondary_input")
        self.secondary_label = QtWidgets.QLabel(self.centralwidget)
        self.secondary_label.setGeometry(QtCore.QRect(10, 150, 91, 21))
        self.secondary_label.setObjectName("secondary_label")
        self.pingButton = QtWidgets.QPushButton(self.centralwidget)
        self.pingButton.setGeometry(QtCore.QRect(10, 280, 71, 27))
        self.pingButton.setObjectName("pingtButton")
        self.current_dns_label = QtWidgets.QLabel(self.centralwidget)
        self.current_dns_label.setGeometry(QtCore.QRect(10, 190, 91, 31))
        self.current_dns_label.setObjectName("current_dns_label")
        self.setButton = QtWidgets.QPushButton(self.centralwidget)
        self.setButton.setGeometry(QtCore.QRect(90, 280, 81, 27))
        self.setButton.setObjectName("setButton")
        self.removeButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeButton.setGeometry(QtCore.QRect(180, 280, 81, 27))
        self.removeButton.setObjectName("removeButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(270, 280, 81, 27))
        self.saveButton.setObjectName("saveButton")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(7, 220, 341, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(9, 239, 341, 31))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.message_label = QtWidgets.QLabel(self.frame)
        self.message_label.setGeometry(QtCore.QRect(10, -2, 321, 31))
        self.message_label.setObjectName("message_label")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(110, 190, 241, 31))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.selected_dns_label_3 = QtWidgets.QLabel(self.centralwidget)
        self.selected_dns_label_3.setGeometry(QtCore.QRect(120, 190, 231, 31))
        self.selected_dns_label_3.setObjectName("selected_dns_label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # signals
        self.retranslateUi(MainWindow)
        self.pingButton.clicked.connect(self.showPing)
        self.saveButton.clicked.connect(self.saveDns)
        self.removeButton.clicked.connect(self.removeDns)
        self.setButton.clicked.connect(self.setDns)
        self.dns_list_box.currentTextChanged['QString'].connect(self.onChangeComboBox)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # select dns when app start
        file = open(os.path.join(sys.path[0], 'lastDns.txt'), 'r')
        lastDns = str(file.read())
        if lastDns in dnsIndexList:
            self.dns_list_box.setCurrentIndex(dnsIndexList.index(lastDns))
            self.selected_dns_label_3.setText(lastDns)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DNS changer"))
        MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(sys.path[0], 'dns-logo.png')))
        self.dns_list_box.setItemText(0, _translate("MainWindow", "New dns"))
        counter = 1
        for dnsName in dnsList:
            self.dns_list_box.setItemText(counter, _translate("MainWindow", dnsName))
            counter += 1
        self.name_label.setText(_translate("MainWindow", "name*:"))
        self.primary_label.setText(_translate("MainWindow", "primary*:"))
        self.secondary_label.setText(_translate("MainWindow", "secondary:"))
        self.pingButton.setText(_translate("MainWindow", "ping"))
        self.current_dns_label.setText(_translate("MainWindow", "my dns:"))
        self.setButton.setText(_translate("MainWindow", "set dns"))
        self.removeButton.setText(_translate("MainWindow", "remove"))
        self.saveButton.setText(_translate("MainWindow", "save"))
        self.message_label.setText(_translate("MainWindow", ""))
        self.selected_dns_label_3.setText(_translate("MainWindow", "not set!"))

    def onChangeComboBox(self, dnsName):
        dnsName = str(dnsName)
        if dnsName == 'New dns':
            self.name_input.setText('')
            self.primary_input.setText('')
            self.secondary_input.setText('')
        else:
            self.name_input.setText(dnsName)
            self.primary_input.setText(dnsList[dnsName][0])
            self.secondary_input.setText(dnsList[dnsName][1])
        self.index = dnsIndexList.index(dnsName)
        self.oldName = dnsName

    def fildCheck(self):
        if self.name_input.text() == '' or self.primary_input.text() == '':
            self.logPrint('fill name and primary fields')
            return True
        elif self.name_input.text() in dnsList:
            if self.name_input.text() == self.oldName and \
                    self.primary_input.text() == dnsList[self.oldName][0] and \
                    self.secondary_input.text() == dnsList[self.oldName][1]:
                self.logPrint("nothing changed")
                return True
            elif self.primary_input.text() == dnsList[self.oldName][0] and \
                    self.secondary_input.text() == dnsList[self.oldName][1]:
                self.logPrint("the name is already exist!")
                return True

    def saveDns(self):
        item_index = self.index
        # check fields (null input or change ...)
        if self.fildCheck():
            return 0

        # check ip validation
        if self.validIPAddress(self.primary_input.text()) == 'Invalid' or \
                (self.secondary_input.text() != '' and self.validIPAddress(self.secondary_input.text()) == 'Invalid'):
            self.logPrint("ip is not valid!")
            return 0

        if self.index == 0:  # if add new dns
            item_index = len(dnsList) + 1
            # add new space in comboBox list
            self.dns_list_box.addItem("")
            dnsIndexList.append(self.name_input.text())
        else:  # if edit dns
            # remove old record
            del dnsList[self.oldName]
            dnsIndexList[self.index] = self.name_input.text()
        # add dns to list
        dnsList[self.name_input.text()] = [
            self.primary_input.text(),
            self.secondary_input.text()
        ]
        # change dns comboBox title
        self.dns_list_box.setItemText(item_index, self.name_input.text())
        # save dns list to file
        file = open(os.path.join(sys.path[0], 'dnsList.json'), "w")
        file.write(json.dumps(dnsList))

        if self.index == 0:
            # add log
            self.logPrint("'" + self.name_input.text() + "' added to list")
            # clear inputs after add new dns
            self.name_input.setText('')
            self.primary_input.setText('')
            self.secondary_input.setText('')
        else:
            # add log
            self.logPrint("'" + self.name_input.text() + "' saved")

    def validIPAddress(self, IP: str) -> str:
        try:
            return "IPv4" if type(ip_address(IP)) is IPv4Address else "IPv6"
        except ValueError:
            return "Invalid"

    def removeDns(self):
        if self.index == 0:
            return 0
        self.logPrint(self.oldName + " removed!")
        # remove item from dict
        del dnsList[self.oldName]
        del dnsIndexList[self.index]
        # remove item from comboBox
        self.dns_list_box.removeItem(self.index)
        # remove item from file
        file = open(os.path.join(sys.path[0], 'dnsList.json'), "w")
        file.write(json.dumps(dnsList))

    # set dns and save it ro resolv.conf file
    def setDns(self):
        if self.index == 0:
            self.logPrint("dns is empty!")
            return 0
        file = open("/etc/resolv.conf", "w")
        # creat resolv.conf text filre
        output = ''
        for i in dnsList[self.oldName]:
            if i != '':
                output += 'nameserver ' + i + "\n"
        # write output in resolv.conf
        file.write(output)
        # change last dns name and write it to lastDns.txt
        file = open(os.path.join(sys.path[0], 'lastDns.txt'), 'w')
        file.write(self.oldName)
        # print log
        self.logPrint('dns changed to ' + self.oldName)
        # change last dns label
        self.selected_dns_label_3.setText(self.oldName)

    # get ping of server
    def ping(self, server='example.com', count=1, wait_sec=1):
        cmd = "ping -c {} -W {} {}".format(count, wait_sec, server).split(' ')
        try:
            output = subprocess.check_output(cmd).decode().strip()
            lines = output.split("\n")
            total = lines[-2].split(',')[3].split()[1]
            loss = lines[-2].split(',')[2].split()[0]
            timing = lines[-1].split()[3].split('/')
            return {
                'type': 'rtt',
                'min': timing[0],
                'avg': timing[1],
                'max': timing[2],
                'mdev': timing[3],
                'total': total,
                'loss': loss,
            }
        except Exception as e:
            print(e)
            return None

    # show ping in label
    def showPing(self):
        if self.index == 0:
            return 0
        dnsPing = self.ping(server=self.primary_input.text(), count=4)
        if dnsPing == None:
            self.logPrint("cant ping " + self.primary_input.text())
        else:
            self.logPrint('avg ping of "' + self.primary_input.text() + '" = ' + dnsPing['avg'] + " ms")

    # log print
    def logPrint(self, text):
        print(text)
        # change message label
        self.message_label.setText(text)


if __name__ == "__main__":
    # load dns list from dnsList.json file
    dnsListFile = open(os.path.join(sys.path[0], 'dnsList.json'), "r")
    dnsList = json.loads(dnsListFile.read())
    dnsList = collections.OrderedDict(sorted(dnsList.items()))
    # create dnsIndexList list
    dnsIndexList = ["New dns"]
    for i in dnsList:
        dnsIndexList.append(i)
    # init app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
