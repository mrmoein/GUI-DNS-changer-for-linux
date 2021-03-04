import datetime
import json
import os
import sys
import threading

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtCore

from utils.mainWindow import Ui_MainWindow
from utils.fast_window import Ui_Dialog
from utils import functions
from utils.data import Data
from ipaddress import ip_address, IPv4Address


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
        # self.ui.name_line_edit.setText(self.data.data['dns_list'][self.data.data['settings']['dns']]['name'])
        # self.ui.primary_line_edit.setText(self.data.data['dns_list'][self.data.data['settings']['dns']]['primary'])
        # self.ui.secondary_line_edit.setText(self.data.data['dns_list'][self.data.data['settings']['dns']]['secondary'])
        # self.ui.dns_selection_combo_box.setCurrentIndex(self.data.data['settings']['dns'])
        # # Set icons
        # self.MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(sys.path[0], "{}/icons/main.png".format(self.path))))
        self.set_button_icon(self.ui.apply_button, '{}/icon/apply.png'.format(self.path))
        self.set_button_icon(self.ui.fastest_button, '{}/icon/fastest.png'.format(self.path))
        self.set_button_icon(self.ui.ping_button, '{}/icon/ping.png'.format(self.path))
        # self.set_button_icon(self.ui.dnsl_list_button, '{}/icon/menu.png'.format(self.path))
        self.set_button_icon(self.ui.save_button, '{}/icon/save.ico'.format(self.path))
        self.set_button_icon(self.ui.remove_button, '{}/icon/remove.png'.format(self.path))
        self.set_button_icon(self.ui.switch_dns_button, '{}/icon/switch.png'.format(self.path))
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
        self.ui.apply_button.clicked.connect(self.a)
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

    def insert_ping_to_fastest_table(self):
        for i in self.ping_results:
            self.fastest.ui.ping_table.removeRow(0)

        self.ping_results.clear()

        lowest = 'fist_check_of_ping'

        for dns in self.data.data['dns_list'][2:]:
            if self.is_fastest_window_closed:
                break
            primary_ping = functions.ping(server=dns['primary'])
            secondary_ping = functions.ping(server=dns['secondary'])
            if primary_ping:
                primary_ping = str(int(float(primary_ping['avg'])))
            else:
                primary_ping = "can't ping!"
            if secondary_ping:
                secondary_ping = str(int(float(secondary_ping['avg'])))
            else:
                secondary_ping = "can't ping!"

            self.ping_results.append({
                "name": dns['name'],
                "primary_ip": dns['primary'],
                "secondary_ip": dns['secondary'],
                "primary_ping": primary_ping,
                "secondary_ping": secondary_ping
            })
            self.add_item_to_table(self.fastest.ui.ping_table, {
                "name": dns['name'],
                "primary_ip": dns['primary'],
                "secondary_ip": dns['secondary'],
                "primary_ping": primary_ping,
                "secondary_ping": secondary_ping
            })

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
                self.data.data['dns_list'].append({
                    "name": self.ui.name_line_edit.text(),
                    "primary": self.ui.primary_line_edit.text(),
                    "secondary": self.ui.secondary_line_edit.text()
                })
                self.ui.dns_selection_combo_box.addItem(self.ui.name_line_edit.text())
            else:
                self.data.data['dns_list'][self.data.data['settings']['dns']]['name'] = self.ui.name_line_edit.text()
                self.data.data['dns_list'][self.data.data['settings']['dns']]['primary'] = self.ui.primary_line_edit.text()
                self.data.data['dns_list'][self.data.data['settings']['dns']]['secondary'] = self.ui.secondary_line_edit.text()
                self.ui.dns_selection_combo_box.setItemText(self.data.data['settings']['dns'], self.ui.name_line_edit.text())
            self.data.save_changes()
            self.send_status_bar_message("{} saved".format(self.ui.name_line_edit.text()))
        else:
            self.send_status_bar_message("something is wrong!")

    def remove_button_clicked(self):
        self.send_status_bar_message("{} removed".format(self.data.data['dns_list'][self.data.data['settings']['dns']]['name']))
        self.data.data['dns_list'].pop()
        self.ui.dns_selection_combo_box.removeItem(self.data.data['settings']['dns'])
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
        self.data.data['dns_list'][self.data.data['settings']['dns']]['primary'] = self.data.data['dns_list'][self.data.data['settings']['dns']]['secondary']
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

    def a(self):
        self.send_status_bar_message("hello")

    # @staticmethod
    # def add_item_to_table(table, stock):
    #     row_count = table.rowCount()
    #     table.setRowCount(row_count + 1)
    #     table.setItem(row_count, 0, QTableWidgetItem(stock['name']))
    #     table.setItem(row_count, 1,
    #                   QTableWidgetItem(str(stock['max_volume'])))
    #     table.setItem(row_count, 2,
    #                   QTableWidgetItem(str(stock['min_volume'])))
    #     timestamp = datetime.datetime.fromtimestamp(stock['timestamp'])
    #     table.setItem(row_count, 3,
    #                   QTableWidgetItem(timestamp.strftime("%H:%M:%S")))

    def end_program(self):
        self.closed = True

    # def on_change(self):
    #     self.db.conn.execute(
    #         "UPDATE settings SET volume_alarm='{}' WHERE id=1;".format(self.ui.volume_alarm_spinBox.value()))
    #     self.db.conn.execute("UPDATE settings SET cool_down='{}' WHERE id=1;".format(self.ui.coolDown_spinBox.value()))
    #     self.db.conn.execute(
    #         "UPDATE settings SET check_from='{}' WHERE id=1;".format(self.ui.check_from_spinBox.value()))
    #     self.settings['volume_alarm'] = self.ui.volume_alarm_spinBox.value()
    #     self.settings['cool_down'] = self.ui.coolDown_spinBox.value()
    #     self.settings['check_from'] = self.ui.check_from_spinBox.value()

    def start(self):
        self.init_main_window()
        self.MainWindow.show()
        self.app.aboutToQuit.connect(self.end_program)
        sys.exit(self.app.exec_())