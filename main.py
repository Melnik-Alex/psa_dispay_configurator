from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from datetime import datetime
from threading import Thread
from time import sleep
from random import randint
import os

response = ''

app = QtWidgets.QApplication([])
ui = uic.loadUi("main.ui")

serial = QSerialPort()
serial.setBaudRate(115200)
serial.clear()
port_list = []
ports = QSerialPortInfo.availablePorts()
for port in ports:
    port_list.append(port.portName())
ui.port_list_combo.addItems(port_list)


def write_to_port_2(data, data_true=False, ):
    print(data)
    if data_true:
        if data is not None:
            data = data + '\n'
            print(f'Sended by user ' + data)
            serial.write(data.encode())
            serial.flush()
        # data_s1 = data_to_send()
        # serial.write(data_s1)
    else:
        data = data + '\n'
        serial.write(data.encode())
        serial.flush()


def write_to_port(data, data_true=False):
    t2 = Thread(target=write_to_port_2(data, data_true=False ))
    t2.start()


# def open_port():
#     serial.setPortName(ui.port_list_combo.currentText())
#     if ui.connect_button.text() == 'Disconnect':
#         write_to_port('C')
#         sleep(1)
#         read_data()
#         sleep(1)
#         serial.close()
#         ui.info_label.setText(f'Port was closed')
#         ui.connect_button.setText('Connect')
#     else:
#         if serial.open(QIODevice.ReadWrite):
#             ui.info_label.setText(f'Open port ' + ui.port_list_combo.currentText() + ' OK!')
#             #ui.connect_button(open_port)
#             ui.connect_button.setText('Disconnect')
#             #ui.comboBox.setEnabled(False)
#             #ui.disconnect.setEnabled(True)
#             #ui.main_control.setEnabled(True)
#             #ui.clear.setEnabled(True)
#             write_to_port('v')
#             sleep(0.5)
#             write_to_port('V')
#             sleep(0.5)
#             write_to_port('CFFFFFF')
#             sleep(0.1)
#             write_to_port('CFFFFFF')
#             write_to_port('CFFFFFF')
#             write_to_port('S4')
#             write_to_port('Z1')
#             write_to_port('O')
#             serial.readAll()
#         else:
#             ui.info_label.setText(f'Connect to Arduino is not success! Select another port and try again')

def open_port():
    serial.setPortName(ui.port_list_combo.currentText())
    if ui.connect_button.text() == 'Disconnect':
        serial.flush()
        write_to_port('C')
        serial.close()
        ui.info_label.setText(f'Port was closed')
        ui.connect_button.setText('Connect')
    else:
        if serial.open(QIODevice.ReadWrite):
            ui.info_label.setText(f'Open port ' + ui.port_list_combo.currentText() + ' OK!')
            ui.connect_button.setText('Disconnect')
            #unlock()
        else:
            ui.info_label.setText(f'Connect to Arduino is not success! Select another port and try again')


def read_data():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    ui.textBrowser.append(str(data))

def read_data_thread():
    global response
    rx = serial.readLine()
    #rx = str(rx, 'utf-8')
    if rx != '':
        #rx = rx.strip()
        #data = rx.split(',')
        ui.textBrowser.append(str(rx))
        response = rx
        print('Yep!')


def send_line():
    text = str(ui.input_line.text().replace(' ', ''))
    text = text.replace('t', '').upper()
    if len(text) == 0:
        print('No data to send')
    else:
        # ui.send_line.clear()
        write_to_port(text, data_true=True)


def get_config():
    ui.textBrowser.append('Config')
    write_to_port('220200')
    sleep(0.5)
    write_to_port('220400')
    sleep(0.5)
    write_to_port('220500')
    sleep(0.5)
    write_to_port('220600')
    sleep(0.5)
    write_to_port('222100')


def unlock():
    global response
    sleep(0.5)
    print('fist')
    write_to_port('>772:672')
    sleep(2)
    print(response)
    if response == b'OK\r\n':
        serial.flush()
        response = ''
        print('pass')
        write_to_port(':ECEC:03:03')

        if str(response) == (str("['5003']")):
            print('pass')
            print(response)
            # ser.write((':ECEC:03:03'+ '\n').encode())
            # sleep(0.5)
            # ser.write(('220200' + '\n').encode())
            # sleep(0.5)
            # ser.write(('220400' + '\n').encode())
            # sleep(0.5)
            # ser.write(('220500' + '\n').encode())
            # sleep(0.5)
            # ser.write(('222100' + '\n').encode())
        else:
            print('not pass')
            print(response)
            # sleep(0.5)
            # ser.write(('1003' + '\n').encode())
    else:
        sleep(0.5)
        print('second')
        serial.flush()
        response = ''
        #write_to_port('>772:672')
    # self.connect_button = True
    # write_to_port('>772:672')
    # write_to_port('1003')
    # write_to_port(':ECEC:03:03')

def loop():
    while True:
        sleep(0.01)
        read_data_thread()

def listener():
    print('lis')
    #Thread(target=read_data_thread).start()
    Thread(target=loop).start()

def unlock_thread():
    t2 = Thread(target=unlock)
    t2.start()


ui.connect_button.pressed.connect(open_port)
ui.pushButton.pressed.connect(listener)
ui.connect_and_unlock.pressed.connect(unlock_thread)
ui.get_config.pressed.connect(get_config)
serial.readyRead.connect(listener)
ui.input_line.returnPressed.connect(send_line)

ui.show()
app.exec()
