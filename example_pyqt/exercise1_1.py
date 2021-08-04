#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
this is an example for PyQt5. in this example, will create a simple window
"""

import sys


from PyQt5.QtWidgets import QApplication, QWidget


def simple_window():
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('simple')
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    simple_window()

