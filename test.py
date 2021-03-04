# coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel

class ChildDlg(QDialog):
   def closeEvent(self, event):
      print("X is clicked")

class mainClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        openDlgBtn = QPushButton("openDlg", self)
        openDlgBtn.clicked.connect(self.openChildDialog)
        openDlgBtn.move(50, 50)

        self.setGeometry(100, 100, 200, 200)
        self.show()

    def openChildDialog(self):
        childDlg = ChildDlg(self)
        childDlgLabel = QLabel("Child dialog", childDlg)

        childDlg.resize(100, 100)
        childDlg.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mc = mainClass()
    sys.exit(app.exec_())