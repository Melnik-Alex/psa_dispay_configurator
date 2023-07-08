__author__ = 'Mehmet Cagri Aksoy - github.com/mcagriaksoy'

import sys, os, serial, serial.tools.list_ports, warnings
from PyQt5.QtCore import *
import time
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from threading import Thread

from time import sleep

response = ''
zones_count = 0


# MULTI-THREADING

class Worker(QObject):
    finished = pyqtSignal(str)
    intReady = pyqtSignal(str)

    @pyqtSlot()
    def __init__(self):
        super(Worker, self).__init__()
        self.working = True

    def work(self):
        global response
        while self.working:
            if ser.isOpen():
                line = ser.readline().decode()
            else:
                line = ''

            if line != '':
                line = line
                time.sleep(0.1)
                self.intReady.emit(line)
                response = line.encode()
                ser.flush()

        self.finished.emit()


class qt(QMainWindow):

    def __init__(self):
        global response
        QMainWindow.__init__(self)
        # loadUi('qt.ui', self)
        loadUi('001.ui', self)

        self.thread = None
        self.worker = None
        self.connect_button.clicked.connect(self.start_loop)
        self.connect_button = False
        self.CopyFlag = 0

    def loop_finished(self):
        print('Loop Finished')

    def start_loop(self):

        mytext = "\n"  # Send first enter
        global ser
        ser = serial.Serial(self.port_list_combo.currentText(), 115200, timeout=1)
        ser.write(mytext.encode())

        self.worker = Worker()  # a new worker to perform those tasks
        self.thread = QThread()  # a new thread to run our background tasks in
        self.worker.moveToThread(
            self.thread)  # move the worker into the thread, do this first before connecting the signals

        self.thread.started.connect(self.worker.work)  # begin our worker object's loop when the thread starts running

        self.worker.intReady.connect(self.onIntReady)

        self.pushButton_2.clicked.connect(self.stop_loop)  # stop the loop on the stop button click

        self.worker.finished.connect(self.loop_finished)  # do something in the gui when the worker loop ends
        self.worker.finished.connect(self.thread.quit)  # tell the thread it's time to stop running
        self.worker.finished.connect(self.worker.deleteLater)  # have worker mark itself for deletion
        self.thread.finished.connect(self.thread.deleteLater)  # have thread mark itself for deletion
        self.thread.start()

    def stop_loop(self):
        self.worker.working = False
        self.label_5.setText("Not Connected")
        self.label_5.setStyleSheet('color: red')
        ser.close()

    def onIntReady(self, i):
        if i != '':
            a = i
            a = str(a).replace("\n", "").replace("\r", "")
            if i[0] + i[1] == '62':
                global zones_count
                if i[2] + i[3] + i[4] + i[5] == '0200':
                    self.textBrowser.append('Zone 0200 was readed!')
                    # print('0200 = ' + i.replace('620200', ''))
                    self.zone_0200.setText(i.replace('620200', ''))
                    zones_count += 1
                if i[2] + i[3] + i[4] + i[5] == '0400':
                    self.textBrowser.append('Zone 0400 was readed!')
                    # print('0400 = ' + i.replace('620400', ''))
                    self.zone_0400.setText(i.replace('620400', ''))
                    zones_count += 1
                if i[2] + i[3] + i[4] + i[5] == '0500':
                    self.textBrowser.append('Zone 0500 was readed!')
                    # print('0500 = ' + i.replace('620500', ''))
                    self.zone_0500.setText(i.replace('620500', ''))
                    zones_count += 1
                if i[2] + i[3] + i[4] + i[5] == '0600':
                    self.textBrowser.append('Zone 0600 was readed!')
                    # print('0600 = ' + i.replace('620600', ''))
                    self.zone_0600.setText(i.replace('620600', ''))
                    zones_count += 1
                if i[2] + i[3] + i[4] + i[5] == '2100':
                    self.textBrowser.append('Zone 2100 was readed!')
                    print('2100 = '+ i.replace('622100', ''))
                    self.zone_2100.setText(i.replace('622100', ''))
                    self.zone_2100_edit_line.setText(i.replace('622100', '').replace(' ',''))
                    zones_count = zones_count + 1
                    if zones_count == 5:
                        self.textBrowser.append('All zones was successfully readed!')
                    else:
                        self.textBrowser.append('Not all zones was successfully readed! Read it again!')
                        self.zone_0200.setText('')
                        self.zone_0400.setText('')
                        self.zone_0500.setText('')
                        self.zone_0600.setText('')
                        self.zone_2100.setText('')
                        zones_count = 0
                        self.read_progress.setValue(zones_count)
                self.read_progress.setValue(zones_count)
            else:
                self.textBrowser.append(a)
                zones_count = 0

    def on_connect_button_clicked(self):
        if self.connect_button:
            self.connect_button = False
            return

        # Port Detection START
        ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'USB' in p.description
        ]

        if not ports:
            ports = ['NONE']

        self.port_list_combo.addItems(ports)
        # Port Detection END

        if ports[0] != 'NONE':
            # Start the progress bar
            # self.completed = 0
            # while self.completed < 100:
            # self.completed += 0.001
            # self.progressBar.setValue(self.completed)
            self.textBrowser.setText('Data Gathering...')
            self.textBrowser.append("CONNECTED!")
            # self.label_5.setStyleSheet('color: green')
            x = 1
            self.textBrowser.setText(":")
        self.connect_button = True

    def on_pushButton_3_clicked(self):
        # Send data from serial port:
        if self.connect_button:
            self.connect_button = False
            return
        mytext = str(self.lineEdit.text().replace(' ', '')) + '\n'
        # mytext = self.lineEdit.toPlainText() + "\n"
        print(mytext.encode())
        ser.write(mytext.encode())
        self.connect_button = True

    def read_data_thread(self):
        global response
        sleep(1)
        ser.write(('>772:672' + '\n').encode())
        sleep(0.5)
        if str(response) == (str(b'OK\r\n')):
            sleep(0.5)
            ser.write(('1003' + '\n').encode())
            sleep(0.2)
            if str(response) == (str(b'5003\r\n')):
                # ser.write((':ECEC:03:03'+ '\n').encode())
                sleep(0.1)
                ser.write(('220200' + '\n').encode())
                sleep(0.05)
                ser.write(('220400' + '\n').encode())
                sleep(0.05)
                ser.write(('220500' + '\n').encode())
                sleep(0.05)
                ser.write(('220600' + '\n').encode())
                sleep(0.05)
                ser.write(('222100' + '\n').encode())
            else:
                sleep(1)
                ser.write(('1003' + '\n').encode())
        else:
            sleep(1)
            ser.write(('>772:672' + '\n').encode())
        self.connect_button = True

    def write_data_thread(self, data):
        global response
        sleep(1)
        ser.write(('1003' + '\n').encode())
        sleep(0.2)
        if str(response) == (str(b'5003\r\n')):
            ser.write((':ECEC:03:03'+ '\n').encode())
            sleep(1)
            ser.write(('2E' + '2100' + data + '\n').encode())
            sleep(0.05)
            ser.write(('2E2901FD000000010101' + '\n').encode())
            sleep(0.05)
            ser.write(('222901' + '\n').encode())
        else:
            sleep(1)
            ser.write(('1003' + '\n').encode())

        self.connect_button = True

    def new_thread(self):
        t1 = Thread(target=self.read_data_thread)
        t1.start()

    def write_thread(self):
        data = self.zone_2100_edit_line.text().replace(' ','')
        if 14 > len(data):
            print('wrong data' + str(len(data)))
            return
        else:
            pass
        if len(data) > 18:
            print('wrong data' + str(len(data)))
            return
        else:
            pass

        t1 = Thread(target=self.write_data_thread(data))
        t1.start()

    def on_read_data_clicked(self):
        # Send data from serial port:
        if self.connect_button:
            self.connect_button = False
            return
        self.new_thread()
        self.textBrowser.setText('Connection')
        self.connect_button = True

    def on_write_button_clicked(self):
        if self.connect_button:
            self.connect_button = False
            return
        self.write_thread()
        self.textBrowser.setText('Writing')
        self.connect_button = True


def run():
    app = QApplication(sys.argv)
    widget = qt()
    serial = QSerialPort()
    serial.setBaudRate(115200)
    serial.clear()
    port_list = []
    ports = QSerialPortInfo.availablePorts()
    for port in ports:
        port_list.append(port.portName())
    widget.port_list_combo.addItems(port_list)
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
