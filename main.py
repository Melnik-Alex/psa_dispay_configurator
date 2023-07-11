import sys, os, serial, serial.tools.list_ports
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
error_write_flag = 0

zone_0200_mem = ''
zone_0400_mem = ''
zone_0500_mem = ''
zone_0600_mem = ''
zone_2100_mem = ''

hw_info = ''
sw_info = ''


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
        global ser
        if self.connect_button_conn.text() == 'Disconnect':
            self.worker.working = False
            self.worker.finished.connect(self.thread.quit)
            ser.close()
            self.info_label.setText('Port ' + self.port_list_combo.currentText() + ' was closed')
            self.info_label.setStyleSheet('color: red')
            self.read_data.setEnabled(False)
            self.connect_to_matrix_screen.setEnabled(False)
            self.read_faults.setEnabled(False)
            self.clear_faults.setEnabled(False)
            self.write_button.setEnabled(False)
            self.config_save.setEnabled(False)
            self.config_load.setEnabled(False)
            self.port_list_combo.setEnabled(True)
            self.group_zones_to_write.setEnabled(False)
            self.connect_button_conn.setText('Connect to port')
            return
        else:
            self.info_label.setStyleSheet('color: green')
            pass
        ports = self.port_list_combo.currentText()

        if ports == '':
            self.info_label.setStyleSheet('color: red')
            self.info_label.setText('No COM port selected!')
            return
        else:
            ser = serial.Serial(self.port_list_combo.currentText(), 115200, timeout=1)
        self.connect_button_conn.setText('Disconnect')
        self.port_list_combo.setEnabled(False)
        self.connect_to_matrix_screen.setEnabled(True)
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
        global error_write_flag
        global hw_info
        global sw_info
        global zone_0200_mem
        global zone_0400_mem
        global zone_0500_mem
        global zone_0600_mem
        global zone_2100_mem
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
                        zone_0200_mem = data_to_zone
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0400':
                    data_to_zone = i.replace('620400', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0400.setText(data_to_zone)
                        self.zone_0401.setText(data_to_zone)
                        self.zone_0401.setEnabled(True)
                        zone_0400_mem = data_to_zone
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0500':
                    data_to_zone = i.replace('620500', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0500.setText(data_to_zone)
                        self.zone_0501.setText(data_to_zone)
                        self.zone_0501.setEnabled(True)
                        zone_0500_mem = data_to_zone
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0600':
                    data_to_zone = i.replace('620600', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0600.setText(data_to_zone)
                        self.zone_0601.setText(data_to_zone)
                        self.zone_0601.setEnabled(True)
                        zone_0600_mem = data_to_zone
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '2100':
                    data_to_zone = i.replace('622100', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_2100.setText(data_to_zone)
                        self.zone_2101.setText(data_to_zone)
                        zone_2100_mem = data_to_zone
                        self.zone_2101.setEnabled(True)
                        self.read_faults.setEnabled(True)
                        self.clear_faults.setEnabled(True)
                        self.config_save.setEnabled(True)
                        self.config_load.setEnabled(True)
                        self.write_button.setEnabled(True)
                        self.group_zones_to_write.setEnabled(True)
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '2901':
                    data_to_zone = i.replace('62', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    print(data_to_zone)

                if i[2] + i[3] == 'F0':
                    if i[4] + i[5] == '80':
                        hw_info = i.replace('62F080', '').replace(' ', '').replace('\r', '').replace('\n', '')
                        if len(hw_info) < 24:
                            pass
                        else:
                            h = hw_info
                            hw_version = h[14] + h[15] + ' ' + h[16] + h[17] + h[18] + ' ' + h[19] + h[20] + h[
                                21] + ' ' + h[22] + h[23]
                            self.hw_label.setText('HW:')
                            self.hw_label_id.setText(hw_version)
                    if i[4] + i[5] == 'FE':
                        sw_info = i.replace('62F0FE', '').replace(' ', '').replace('\r', '').replace('\n', '')
                        if len(sw_info) < 19:
                            pass
                        else:
                            s = sw_info
                            sw_version = '96 ' + s[14] + s[15] + s[16] + ' ' + s[17] + s[18] + s[19] + ' 80'
                            self.sw_label.setText('SW:')
                            self.sw_label_id.setText(sw_version)

                else:
                    self.textBrowser.append(a)

            elif i[0] + i[1] == '6E':
                data_from_zone = i[2] + i[3] + i[4] + i[5]
                response_success = i

            elif i[0] + i[1] == '7F':
                if i[2] + i[3]+ i[4]+ i[5] == '2E31':
                    error_write_flag += 1
                    self.info_label.setStyleSheet('color: red')
                    self.textBrowser.append('Write data error. Trying ' + str(error_write_flag) + ' from 5')
                else:
                    response_success = i
                    self.textBrowser.append(a)
                response_success = i

            else:
                self.textBrowser.append(a)

    def on_connect_button_conn_clicked(self):
        if self.connect_button:
            self.connect_button = False
            return

        # Port Detection START
        ports = self.port_list_combo.currentText()

        if ports == '':
            self.info_label.setStyleSheet('color: red')
            self.info_label.setText('No COM port selected!')
            return
        # Port Detection END

        if ports[0]:
            x = 1
            self.info_label.setStyleSheet('color: red')
            self.info_label.setText('Connected to com port ' + self.port_list_combo.currentText() + '!')
        self.connect_button = True

    def on_pushButton_3_clicked(self):
        # Send data from serial port:
        if self.connect_button:
            self.connect_button = False
            return
        mytext = str(self.lineEdit.text().replace(' ', '')) + '\n'
        ser.write(mytext.encode())
        self.connect_button = True

    def write_zone(self, zone, data_to_write):
        if self.connect_button:
            self.connect_button = False
        # Writing zones to LCD
        global zones_write_count
        global error_write_flag
        emergency_end = False
        ser.flush()
        sleep(0.05)
        self.textBrowser.append('Writing zone ' + zone)
        write_str = ('2E' + zone + data_to_write + '\n').encode()
        ser.write(write_str)
        resp = 0
        error_write_flag = 0
        while str(response) != (str(b'6E' + zone.encode() + b'\r\n')):
            resp += 1
            sleep(0.01)
            if resp == 100:
                resp = 0
                #ser.flush()
                ser.write(('2E' + zone + data_to_write + '\n').encode())
            if error_write_flag == 5:  # Exit by timeout
                emergency_end = True
                self.textBrowser.append('Zone ' + zone + ' was NOT written!')
                self.textBrowser.setStyleSheet('color: red')
                error_write_flag = 0
                self.connect_button = True
                break
        resp = 0

        zones_write_count += 1
        # self.write_progress.setValue(zones_write_count)
        if zone == '2901':
            self.textBrowser.append('Security zone was written!')
        else:
            if emergency_end:
                pass
            else:
                self.textBrowser.append('Zone ' + zone + ' was written!')
                self.textBrowser.setStyleSheet('color: green')
        self.connect_button = True

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
            ser.flush()
            sleep(0.1)
            ser.write(write_str)

        zones_count += 1
        self.read_progress.setValue(zones_count)
        self.textBrowser.append('Zone ' + zone + ' was readed!')

    def unlock_before_read_data(self):
        # First unlock of Arduino
        global hw_info
        global sw_info
        global response
        ser.flush()
        sleep(0.05)
        ser.write(('>772:672' + '\n').encode())
        resp = 0
        while str(response) != (str(b'OK\r\n')):
            resp += 1
            sleep(0.01)
            if resp == 100:
                resp = 0
                ser.flush()
                ser.write(('>772:672' + '\n').encode())
        resp = 0
        if str(response) == (str(b'OK\r\n')):
            ser.flush()
            sleep(0.05)
            ser.write(('1003' + '\n').encode())
            while str(response) != (str(b'5003\r\n')):
                resp += 1
                sleep(0.01)
                if resp == 100:
                    resp = 0
                    ser.flush()
                    ser.write(('1003' + '\n').encode())
            if str(response) == (str(b'5003\r\n')):
                if hw_info == '':
                    ser.write(('22F080' + '\n').encode())
                    sleep(0.1)
                if sw_info == '':
                    ser.write(('22F0FE' + '\n').encode())
                    sleep(0.1)
        self.read_data.setEnabled(True)
        self.info_label.setText('Connected to matrix screen!')
        self.connect_button = True

    def read_data_thread(self):
        global response
        self.unlock_before_read_data()
        self.read_zone(zone='0200')
        sleep(0.1)
        self.read_zone(zone='0400')
        sleep(0.1)
        self.read_zone(zone='0500')
        sleep(0.1)
        self.read_zone(zone='0600')
        sleep(0.1)
        self.read_zone(zone='2100')
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
        if self.connect_button:
            self.connect_button = False
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

    def unlock_for_read_thread(self):
        ser.flush()
        t3 = Thread(target=self.unlock_before_read_data)
        t3.start()

    def on_connect_to_matrix_screen_clicked(self):
        self.unlock_for_read_thread()

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

    def on_clear_faults_clicked(self):
        # Clearing faults
        self.textBrowser.setStyleSheet('color: black')
        if self.connect_button:
            self.connect_button = False
            return
        self.textBrowser.setText('')
        ser.flush()
        ser.write(('14FFFFFF' + '\n').encode())
        self.connect_button = True

    def on_read_faults_clicked(self):
        # Reading faults
        self.textBrowser.setStyleSheet('color: black')
        if self.connect_button:
            self.connect_button = False
            return
        self.textBrowser.setText('')
        ser.flush()
        ser.write(('190209' + '\n').encode())
        self.connect_button = True

    def open_config_tread(self):
        global hw_info
        global sw_info
        global zone_0200_mem
        global zone_0400_mem
        global zone_0500_mem
        global zone_0600_mem
        global zone_2100_mem
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open configuration file", "",
                                                  "PSA screen config file (*.matt)", options=options)
        if fileName:
            file = open(fileName, 'r')
            hw_info = file.readline().replace('\n', '').replace('\r', '')
            sw_info = file.readline().replace('\n', '').replace('\r', '')
            zone_0200_mem = file.readline().replace('\n', '').replace('\r', '')
            zone_0400_mem = file.readline().replace('\n', '').replace('\r', '')
            zone_0500_mem = file.readline().replace('\n', '').replace('\r', '')
            zone_0600_mem = file.readline().replace('\n', '').replace('\r', '')
            zone_2100_mem = file.readline().replace('\n', '').replace('\r', '')
            self.zone_0201.setText(zone_0200_mem)
            self.zone_0401.setText(zone_0400_mem)
            self.zone_0501.setText(zone_0500_mem)
            self.zone_0601.setText(zone_0600_mem)
            self.zone_2101.setText(zone_2100_mem)
            file.close()
            return

    def write_config_tread(self):
        global hw_info
        global sw_info
        global zone_0200_mem
        global zone_0400_mem
        global zone_0500_mem
        global zone_0600_mem
        global zone_2100_mem
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save configuration file", "",
                                                  "PSA screen config file (*.matt)", options=options)
        if fileName:
            file = open(fileName, 'w')
            file.write(hw_info + '\n')
            file.write(sw_info + '\n')
            file.write(zone_0200_mem + '\n')
            file.write(zone_0400_mem + '\n')
            file.write(zone_0500_mem + '\n')
            file.write(zone_0600_mem + '\n')
            file.write(zone_2100_mem + '\n')
            file.close()

    def on_config_load_clicked(self):
        if self.connect_button:
            self.connect_button = False
            return
        t4 = Thread(target=self.open_config_tread())
        t4.start()
        self.connect_button = True

    def on_config_save_clicked(self):
        if self.connect_button:
            self.connect_button = False
            return
        t5 = Thread(target=self.write_config_tread())
        t5.start()
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
