#! /usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QIcon

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon exmaple')
        self.setWindowIcon(QIcon('exercise1_2_pic.png'))
        self.show()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())