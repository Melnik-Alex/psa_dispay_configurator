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
response_success = ''
zones_count = 0
zones_write_count = 0


# MULTI-THREADING

class Worker(QObject):
    finished = pyqtSignal()
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
        global response_success
        QMainWindow.__init__(self)
        # loadUi('qt.ui', self)
        loadUi('001.ui', self)

        self.thread = None
        self.worker = None
        self.connect_button_conn.clicked.connect(self.start_loop)
        self.connect_button = False
        self.CopyFlag = 0

    def start_loop(self):
        #mytext = "\n"  # Send first enter
        global ser
        if self.connect_button_conn.text() == 'Disconnect':
            self.worker.working = False
            self.worker.finished.connect(self.thread.quit)
            ser.close()
            self.textBrowser.setText('Port '+self.port_list_combo.currentText()+' was closed')
            self.textBrowser.setStyleSheet('color: red')
            self.read_data.setEnabled(False)
            self.port_list_combo.setEnabled(True)
            self.group_zones_to_write.setEnabled(False)
            self.connect_button_conn.setText('Connect')
            return
        else:
            self.textBrowser.setStyleSheet('color: black')
            pass
        ser = serial.Serial(self.port_list_combo.currentText(), 115200, timeout=1)
        self.connect_button_conn.setText('Disconnect')
        self.port_list_combo.setEnabled(False)
        self.read_data.setEnabled(True)
        self.worker = Worker()  # a new worker to perform those tasks
        self.thread = QThread()  # a new thread to run our background tasks in
        self.worker.moveToThread(
            self.thread)  # move the worker into the thread, do this first before connecting the signals
        self.thread.started.connect(self.worker.work)  # begin our worker object's loop when the thread starts running

        self.worker.intReady.connect(self.onIntReady)

        self.worker.finished.connect(self.thread.quit)  # tell the thread it's time to stop running
        self.worker.finished.connect(self.worker.deleteLater)  # have worker mark itself for deletion
        self.thread.finished.connect(self.thread.deleteLater)  # have thread mark itself for deletion
        self.thread.start()


    def onIntReady(self, i):
        global response_success
        if i != '':
            a = i
            a = str(a).replace("\n", "").replace("\r", "")
            if i[0] + i[1] == '62':
                if i[2] + i[3] + i[4] + i[5] == '0200':
                    data_to_zone = i.replace('620200', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0200.setText(data_to_zone)
                        self.zone_0201.setText(data_to_zone)
                        self.zone_0201.setEnabled(True)
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0400':
                    data_to_zone = i.replace('620400', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0400.setText(data_to_zone)
                        self.zone_0401.setText(data_to_zone)
                        self.zone_0401.setEnabled(True)
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0500':
                    data_to_zone = i.replace('620500', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0500.setText(data_to_zone)
                        self.zone_0501.setText(data_to_zone)
                        self.zone_0501.setEnabled(True)
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0600':
                    data_to_zone = i.replace('620600', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0600.setText(data_to_zone)
                        self.zone_0601.setText(data_to_zone)
                        self.zone_0601.setEnabled(True)
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '2100':
                    data_to_zone = i.replace('622100', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_2100.setText(data_to_zone)
                        self.zone_2101.setText(data_to_zone)
                        self.zone_2101.setEnabled(True)
                        self.write_button.setEnabled(True)
                        self.group_zones_to_write.setEnabled(True)
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '2901':
                    data_to_zone = i.replace('62', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    print(data_to_zone)

            elif i[0] + i[1] == '6E':
                data_from_zone = i[2] + i[3] + i[4] + i[5]
                response_success = i

            else:
                self.textBrowser.append(a)

    def on_connect_button_conn_clicked(self):
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
        # Port Detection END

        if ports[0] != 'NONE':
            x = 1
            self.textBrowser.setText('Port '+self.port_list_combo.currentText()+' opened successfully')
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

    def write_zone(self, zone, data_to_write):
        # Writing zones to LCD
        global zones_write_count
        ser.flush()
        sleep(0.05)
        write_str = ('2E' + zone + data_to_write + '\n').encode()
        print(write_str)
        ser.write(write_str)
        resp = 0
        while str(response) != (str(b'6E' + zone.encode() + b'\r\n')):
            resp += 1
            sleep(0.01)
            if resp == 100:
                resp = 0
                ser.flush()
                ser.write(('2E' + zone + data_to_write + '\n').encode())
        resp = 0

        zones_write_count += 1
        self.write_progress.setValue(zones_write_count)
        if zone == '2901':
            self.textBrowser.append('Security zone was written!')
        else:
            self.textBrowser.append('Zone ' + zone + ' was written!')

    def read_zone(self, zone):
        # Reading zones from LCD
        global zones_count
        ser.flush()
        zone_name = f'self.zone_{zone}'
        eval(zone_name).setText(' ')
        sleep(0.05)
        write_str = ('22' + zone + '\n').encode()
        ser.write(write_str)
        while eval(zone_name).text() == ' ' and not (float(len(eval(zone_name).text())) / 2).is_integer():
            # print('Trying to read zone ' +zone)
            ser.flush()
            sleep(0.1)
            ser.write(write_str)
            # print(float(len(eval(zone_name).text())))

        zones_count += 1
        self.read_progress.setValue(zones_count)
        self.textBrowser.append('Zone ' + zone + ' was readed!')

    def read_data_thread(self):
        global response
        sleep(1)
        ser.flush()
        ser.write(('>772:672' + '\n').encode())
        sleep(0.5)
        while str(response) != (str(b'OK\r\n')):
            ser.flush()
            sleep(0.5)
            ser.write(('>772:672' + '\n').encode())
            sleep(0.5)
        if str(response) == (str(b'OK\r\n')):
            ser.flush()
            sleep(0.5)
            ser.write(('1003' + '\n').encode())
            sleep(0.2)
            while str(response) != (str(b'5003\r\n')):
                ser.flush()
                sleep(0.5)
                ser.write(('1003' + '\n').encode())
                sleep(0.2)
            if str(response) == (str(b'5003\r\n')):
                sleep(0.1)
                self.read_zone(zone='0200')
                sleep(0.1)
                self.read_zone(zone='0400')
                sleep(0.1)
                self.read_zone(zone='0500')
                sleep(0.1)
                self.read_zone(zone='0600')
                sleep(0.1)
                self.read_zone(zone='2100')
            else:
                sleep(1)
                ser.write(('1003' + '\n').encode())
        else:
            sleep(1)
            ser.write(('>772:672' + '\n').encode())
        self.connect_button = True

    def unlock_display(self):
        ser.flush()
        sleep(0.5)
        ser.write(('1003' + '\n').encode())
        sleep(0.2)
        while str(response) != (str(b'5003\r\n')):
            ser.flush()
            sleep(0.5)
            ser.write(('1003' + '\n').encode())
            sleep(0.2)
        if str(response) == (str(b'5003\r\n')):
            ser.write((':ECEC:03:03' + '\n').encode())
            sleep(1)

    def write_data_thread(self):
        global zones_write_count
        data_0200 = self.zone_0201.text().replace(' ', '').replace('\r', '').replace('\n', '')
        data_0400 = self.zone_0401.text().replace(' ', '').replace('\r', '').replace('\n', '')
        data_0500 = self.zone_0501.text().replace(' ', '').replace('\r', '').replace('\n', '')
        data_0600 = self.zone_0601.text().replace(' ', '').replace('\r', '').replace('\n', '')
        data_2100 = self.zone_2101.text().replace(' ', '').replace('\r', '').replace('\n', '')
        if 14 > len(data_2100):
            self.textBrowser.setText(
                'Data too short - ' + str(len(data_2100)) + ' symbols.' + '\n' + 'Expected more (14 max)')
            return
        else:
            pass
        if len(data_2100) > 18:
            self.textBrowser.setText(
                'Data too long - ' + str(len(data_2100)) + ' symbols' + '\n' + 'Expected less (18 max)')
            return
        else:
            pass
        self.unlock_display()
        self.textBrowser.append('Display unlocked')
        ser.flush()
        sleep(1)
        self.textBrowser.append('Start writing')
        self.write_zone(zone='0200', data_to_write=data_0200)
        self.write_zone(zone='0400', data_to_write=data_0400)
        self.write_zone(zone='0500', data_to_write=data_0500)
        self.write_zone(zone='0600', data_to_write=data_0600)
        self.write_zone(zone='2100', data_to_write=data_2100)
        self.write_zone(zone='2901', data_to_write='FD000000010101')
        ser.write(('222901' + '\n').encode())

        zones_write_count = 0
        self.connect_button = True


    def new_thread(self):
        global zones_count
        zones_count = 0
        self.read_progress.setValue(zones_count)
        t1 = Thread(target=self.read_data_thread)
        t1.start()

    def write_thread(self):
        ser.flush()
        t2 = Thread(target=self.write_data_thread)
        t2.start()

    def on_read_data_clicked(self):
        # Send data from serial port:
        self.textBrowser.setStyleSheet('color: black')
        if self.connect_button:
            self.connect_button = False
            return
        self.new_thread()
        self.textBrowser.setText('Connection')
        self.connect_button = True

    def on_write_button_clicked(self):
        # Write zones to LCD
        self.textBrowser.setStyleSheet('color: black')
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
