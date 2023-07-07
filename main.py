from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from datetime import datetime
import threading
from time import sleep
from random import randint
import os


app = QtWidgets.QApplication([])
ui = uic.loadUi("main.ui")

ui.show()
app.exec()