import os
import sys
import threading
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import *
from utils.mainWindow import Ui_MainWindow
from utils.fast_window import Ui_Dialog
from utils import functions
from utils.data import Data
from ipaddress import ip_address, IPv4Address
# import simpleaudio as sa


class GUI:
    def __init__(self, path):
        self.closed = False
        self.statusBar_is_hide = True
        self.path = path
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.data = Data('{}/utils/data.json'.format(path))
        # ------------
        self.fastest = QDialog()
        self.fastest.ui = Ui_Dialog()
        self.fastest.ui.setupUi(self.fastest)
        self.init_fastest_window()
        self.ping_results = []
        self.is_fastest_window_closed = False

    def init_main_window(self):
        # Set icons
        self.set_button_icon(self.ui.apply_button, '{}/icon/apply.png'.format(self.path))
        self.set_button_icon(self.ui.fastest_button, '{}/icon/fastest.png'.format(self.path))
        self.set_button_icon(self.ui.ping_button, '{}/icon/ping.png'.format(self.path))
        # self.set_button_icon(self.ui.dnsl_list_button, '{}/icon/menu.png'.format(self.path))
        self.set_button_icon(self.ui.save_button, '{}/icon/save.ico'.format(self.path))
        self.set_button_icon(self.ui.remove_button, '{}/icon/remove.png'.format(self.path))
        self.set_button_icon(self.ui.switch_dns_button, '{}/icon/switch.png'.format(self.path))
        self.MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(sys.path[0], "{}/icon/dns-logo.png".format(self.path))))
        # Init statusbar
        self.ui.statusBar = QtWidgets.QStatusBar(self.MainWindow)
        self.ui.statusBar.setObjectName("statusBar")
        self.MainWindow.setStatusBar(self.ui.statusBar)
        self.ui.statusBar.hide()
        self.ui.statusBar.setStyleSheet('color: #ffffff; background-color: #404040')
        # Load dns combo box list
        for dns in self.data.data['dns_list']:
            self.ui.dns_selection_combo_box.addItem(dns['name'])
        self.select_dns_combo_box_changed(self.data.data['settings']['dns'])
        # Signals
        self.ui.apply_button.clicked.connect(self.apply_dns)
        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.ping_button.clicked.connect(self.calc_current_dns_ping)
        self.ui.remove_button.clicked.connect(self.remove_button_clicked)
        self.ui.fastest_button.clicked.connect(self.start_fastest_window)
        self.ui.primary_line_edit.textChanged.connect(self.primary_changed)
        self.ui.secondary_line_edit.textChanged.connect(self.secondary_changed)
        self.ui.dns_selection_combo_box.currentIndexChanged.connect(self.select_dns_combo_box_changed)
        self.ui.switch_dns_button.clicked.connect(self.switch_dns_button_clicked)

    def add_item_to_table(self, table, dns):
        row_count = table.rowCount()
        table.setRowCount(row_count + 1)
        table.setItem(row_count, 0, QTableWidgetItem(dns['name']))
        table.setItem(row_count, 1, QTableWidgetItem(dns['primary_ip']))
        table.setItem(row_count, 2, QTableWidgetItem(dns['secondary_ip']))
        table.setItem(row_count, 3, QTableWidgetItem(dns['primary_ping']))
        table.setItem(row_count, 4, QTableWidgetItem(dns['secondary_ping']))

    def init_fastest_window(self):
        self.fastest.ui.ping_table.setColumnCount(5)
        self.fastest.ui.ping_table.setHorizontalHeaderLabels(
            ["name", "primary ip", "secondary ip", "primary ping", "secondary ping"])
        self.fastest.ui.ping_table.horizontalHeader().setStretchLastSection(True)
        self.fastest.ui.ping_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.fastest.ui.ok_button.clicked.connect(self.ok_button_clicked)
        self.fastest.finished['int'].connect(self.fastest_window_closed)

    def ok_button_clicked(self):
        self.fastest.close()
        self.is_fastest_window_closed = True

    def start_fastest_window(self):
        self.is_fastest_window_closed = False
        self.fastest.show()
        threading.Thread(target=self.insert_ping_to_fastest_table).start()
        self.fastest.exec_()

    def fastest_window_closed(self):
        self.is_fastest_window_closed = True

    @staticmethod
    def get_ping_text(ping):
        if ping:
            return int(float(ping['avg']))
        else:
            return "can't ping!"

    def insert_ping_to_fastest_table(self):
        for i in self.ping_results:
            self.fastest.ui.ping_table.removeRow(0)

        self.ping_results.clear()

        for dns in self.data.data['dns_list'][2:]:
            if self.is_fastest_window_closed:
                break
            # get ping of dns
            primary_ping = functions.ping(server=dns['primary'])
            secondary_ping = functions.ping(server=dns['secondary'])
            # check if ping not False
            primary_ping = self.get_ping_text(primary_ping)
            secondary_ping = self.get_ping_text(secondary_ping)
            # find the lowest ping for this dns
            if (isinstance(primary_ping, int) and isinstance(secondary_ping, int)) and primary_ping < secondary_ping:
                lowest_ping = primary_ping
            elif (isinstance(primary_ping, int) and isinstance(secondary_ping, int)) and primary_ping > secondary_ping:
                lowest_ping = secondary_ping
            elif isinstance(primary_ping, int):
                lowest_ping = primary_ping
            else:
                lowest_ping = secondary_ping
            # add dns to temp list
            self.ping_results.append({
                "name": dns['name'],
                "primary_ip": dns['primary'],
                "secondary_ip": dns['secondary'],
                "primary_ping": str(primary_ping),
                "secondary_ping": str(secondary_ping),
                "lowest_ping": lowest_ping
            })
            self.add_item_to_table(self.fastest.ui.ping_table, {
                "name": dns['name'],
                "primary_ip": dns['primary'],
                "secondary_ip": dns['secondary'],
                "primary_ping": str(primary_ping),
                "secondary_ping": str(secondary_ping)
            })
        # clear table
        for i in self.ping_results:
            self.fastest.ui.ping_table.removeRow(0)
        # sort by lowest ping
        sorted_ping_results = sorted(self.ping_results, key=lambda k: k['lowest_ping'])
        # create final table
        for dns in sorted_ping_results:
            self.add_item_to_table(self.fastest.ui.ping_table, {
                "name": dns['name'],
                "primary_ip": dns['primary_ip'],
                "secondary_ip": dns['secondary_ip'],
                "primary_ping": dns['primary_ping'],
                "secondary_ping": dns['secondary_ping']
            })
        # play complete sound
        # print('{}/sounds/insight-578.wav'.format(self.path))
        # sa.WaveObject.from_wave_file('{}/sounds/insight-578.wav'.format(self.path)).play()

    @staticmethod
    def valid_ip_address(ip):
        try:
            if type(ip_address(ip)) is IPv4Address:
                return True
        except ValueError:
            return False

    def save_button_clicked(self):
        if self.ui.primary_line_edit.text() != '':
            primary = self.valid_ip_address(self.ui.primary_line_edit.text())
        else:
            primary = False
        if self.ui.secondary_line_edit.text() != '':
            secondary = self.valid_ip_address(self.ui.secondary_line_edit.text())
        else:
            secondary = False

        if primary or secondary:
            if self.data.data['settings']['dns'] == 1:
                # if new dns
                self.data.data['dns_list'].append({
                    "name": self.ui.name_line_edit.text(),
                    "primary": self.ui.primary_line_edit.text(),
                    "secondary": self.ui.secondary_line_edit.text()
                })
                self.ui.dns_selection_combo_box.addItem(self.ui.name_line_edit.text())
                self.ui.dns_selection_combo_box.setCurrentIndex(len(self.data.data['dns_list']) - 1)
            else:
                self.data.data['dns_list'][self.data.data['settings']['dns']]['name'] = self.ui.name_line_edit.text()
                self.data.data['dns_list'][self.data.data['settings']['dns']][
                    'primary'] = self.ui.primary_line_edit.text()
                self.data.data['dns_list'][self.data.data['settings']['dns']][
                    'secondary'] = self.ui.secondary_line_edit.text()
                self.ui.dns_selection_combo_box.setItemText(self.data.data['settings']['dns'],
                                                            self.ui.name_line_edit.text())
            self.data.save_changes()
            self.send_status_bar_message("{} saved".format(self.ui.name_line_edit.text()))
        else:
            self.send_status_bar_message("something is wrong!")

    def remove_button_clicked(self):
        need_remove_dns_name = self.data.data['dns_list'][self.data.data['settings']['dns']]['name']
        counter = 0
        self.send_status_bar_message(
            "{} removed".format(self.data.data['dns_list'][self.data.data['settings']['dns']]['name']))
        for dns in self.data.data['dns_list']:
            if dns['name'] == need_remove_dns_name:
                self.data.data['dns_list'].pop(counter)
                break
            counter += 1
        self.ui.dns_selection_combo_box.removeItem(self.data.data['settings']['dns'])
        self.select_dns_combo_box(0)
        self.data.save_changes()
        
    def primary_changed(self):
        if self.valid_ip_address(self.ui.primary_line_edit.text()):
            self.ui.primary_line_edit.setStyleSheet('color: #009933')
        else:
            self.ui.primary_line_edit.setStyleSheet('color: #e60000')

    def secondary_changed(self):
        if self.valid_ip_address(self.ui.secondary_line_edit.text()):
            self.ui.secondary_line_edit.setStyleSheet('color: #009933')
        else:
            self.ui.secondary_line_edit.setStyleSheet('color: #e60000')

    def send_status_bar_message(self, text):
        if self.statusBar_is_hide:
            self.statusBar_is_hide = False
            self.ui.statusBar.show()
        self.ui.statusBar.showMessage(text)

    def calc_current_dns_ping(self):
        primary_ping = functions.ping(server=self.ui.primary_line_edit.text())
        secondary_ping = functions.ping(server=self.ui.secondary_line_edit.text())

        if primary_ping:
            primary_ping = int(float(primary_ping['avg']))
        else:
            primary_ping = 'not found'
        if secondary_ping:
            secondary_ping = int(float(secondary_ping['avg']))
        else:
            secondary_ping = 'not found'

        self.send_status_bar_message('{} => primary: {} | secondary: {}'.format(
            self.data.data['dns_list'][self.data.data['settings']['dns']]['name'],
            primary_ping,
            secondary_ping
        ))

    def select_dns_combo_box(self, index):
        if index == 1:
            self.ui.remove_button.setDisabled(True)
            self.ui.primary_line_edit.setDisabled(False)
            self.ui.secondary_line_edit.setDisabled(False)
            self.ui.switch_dns_button.setDisabled(True)
            self.ui.name_line_edit.setDisabled(False)
            self.ui.dns_selection_combo_box.setCurrentIndex(index)
        elif index == 0:
            self.ui.primary_line_edit.setDisabled(True)
            self.ui.secondary_line_edit.setDisabled(True)
            self.ui.switch_dns_button.setDisabled(True)
            self.ui.name_line_edit.setDisabled(True)
            self.ui.remove_button.setDisabled(True)
            self.ui.dns_selection_combo_box.setCurrentIndex(index)
        else:
            self.ui.primary_line_edit.setDisabled(False)
            self.ui.secondary_line_edit.setDisabled(False)
            self.ui.switch_dns_button.setDisabled(False)
            self.ui.name_line_edit.setDisabled(False)
            self.ui.remove_button.setDisabled(False)
            self.ui.dns_selection_combo_box.setCurrentIndex(index)

    def switch_dns_button_clicked(self):
        primary = self.data.data['dns_list'][self.data.data['settings']['dns']]['primary']
        self.data.data['dns_list'][self.data.data['settings']['dns']]['primary'] = \
        self.data.data['dns_list'][self.data.data['settings']['dns']]['secondary']
        self.data.data['dns_list'][self.data.data['settings']['dns']]['secondary'] = primary
        self.select_dns_combo_box_changed(self.data.data['settings']['dns'])
        self.data.save_changes()

    def select_dns_combo_box_changed(self, index):
        self.select_dns_combo_box(index)
        self.ui.name_line_edit.setText(self.data.data['dns_list'][index]['name'])
        self.ui.primary_line_edit.setText(self.data.data['dns_list'][index]['primary'])
        self.ui.secondary_line_edit.setText(self.data.data['dns_list'][index]['secondary'])
        self.data.data['settings']['dns'] = index
        self.data.save_changes()

    @staticmethod
    def set_button_icon(button, icon_path):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)

    def apply_dns(self):
        try:
            file = open("/etc/resolv.conf", "w+")
            # creat resolv.conf text file
            output = ''

            if self.data.data['dns_list'][self.data.data['settings']['dns']]['primary']:
                output += 'nameserver ' + self.data.data['dns_list'][self.data.data['settings']['dns']]['primary'] + "\n"
            if self.data.data['dns_list'][self.data.data['settings']['dns']]['secondary']:
                output += 'nameserver ' + self.data.data['dns_list'][self.data.data['settings']['dns']]['secondary'] + "\n"
            # write output in resolv.conf
            file.write(output)
            file.close()
            self.send_status_bar_message("{} applied successfully".format(self.data.data['dns_list'][self.data.data['settings']['dns']]['name']))
        except Exception as e:
            print(e)
            self.send_status_bar_message(str(e))
            functions.print_c("can't apply DNS!", functions.Bcolors.FAIL)

    def end_program(self):
        self.closed = True

    def start(self):
        self.init_main_window()
        self.MainWindow.show()
        self.app.aboutToQuit.connect(self.end_program)
        sys.exit(self.app.exec_())
