import sys, os, serial, serial.tools.list_ports
from PyQt5.QtCore import *
import time
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from threading import Thread

from time import sleep

from Data.converter import Converter
from Data.sender import Sender

response = ''
response_success = ''
zones_count = 0
zones_write_count = 0
zones_progress_bar_len = 1

zone_0200_mem = ''
zone_0400_mem = ''
zone_0500_mem = ''
zone_0600_mem = ''
zone_2100_mem = ''

zone_0200_read = ''
zone_0400_read = ''
zone_0500_read = ''
zone_0600_read = ''
zone_2100_read = ''

data_0200 = ''
data_0400 = ''
data_0500 = ''
data_0600 = ''
data_2100 = ''

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
        loadUi('app_data/main.ui', self)

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
            self.connect_to_matrix_screen.setStyleSheet('color: gray')
            self.connect_to_matrix_screen.setText('Connect to matrix screen')
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
        self.connect_to_matrix_screen.setStyleSheet('color: black')
        self.connect_to_matrix_screen.setText('Connect to matrix screen')
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
        global hw_info
        global sw_info
        global zone_0200_mem
        global zone_0400_mem
        global zone_0500_mem
        global zone_0600_mem
        global zone_2100_mem
        global zone_0200_read
        global zone_0400_read
        global zone_0500_read
        global zone_0600_read
        global zone_2100_read
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
                        zone_0200_read = data_to_zone
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0400':
                    data_to_zone = i.replace('620400', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0400.setText(data_to_zone)
                        self.zone_0401.setText(data_to_zone)
                        self.zone_0401.setEnabled(True)
                        zone_0400_mem = data_to_zone
                        zone_0400_read = data_to_zone
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0500':
                    data_to_zone = i.replace('620500', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0500.setText(data_to_zone)
                        self.zone_0501.setText(data_to_zone)
                        self.zone_0501.setEnabled(True)
                        zone_0500_mem = data_to_zone
                        zone_0500_read = data_to_zone
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '0600':
                    data_to_zone = i.replace('620600', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_0600.setText(data_to_zone)
                        self.zone_0601.setText(data_to_zone)
                        self.zone_0601.setEnabled(True)
                        zone_0600_mem = data_to_zone
                        zone_0600_read = data_to_zone
                    else:
                        pass
                if i[2] + i[3] + i[4] + i[5] == '2100':
                    data_to_zone = i.replace('622100', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if float(len(data_to_zone) / 2).is_integer():
                        self.zone_2100.setText(data_to_zone)
                        self.zone_2101.setText(data_to_zone)
                        zone_2100_mem = data_to_zone
                        zone_2100_read = data_to_zone
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
                    # print(data_to_zone)

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
                    # self.textBrowser.append(a)
                    pass

            elif i[0] + i[1] == '6E':
                data_from_zone = i[2] + i[3] + i[4] + i[5]
                response_success = i

            elif i[0] + i[1] == '59':
                if i[2] + i[3] + i[4] + i[5] == '0209':
                    faults = i.replace('590209', '').replace(' ', '').replace('\r', '').replace('\n', '')
                    if faults == '':
                        faults = 'No faults!'
                        self.fault_row.setStyleSheet('color: green')
                    else:
                        self.fault_row.setStyleSheet('color: red')
                    self.fault_row.setText(faults)
                else:
                    pass

            elif i[0] + i[1] == '54':
                self.fault_row.setText('Faults cleared')
                self.fault_row.setStyleSheet('color: green')


            else:
                # self.textBrowser.append(a)
                pass

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
        # Writing zones to LCD
        global zones_write_count
        ser.flush()
        sleep(0.05)
        write_str = ('2E' + zone + data_to_write + '\n').encode()
        ser.write(write_str)
        resp = 0
        emergency_stop = 0
        trying_count = 0
        while str(response) != (str(b'6E' + zone.encode() + b'\r\n')):
            resp += 1
            emergency_stop += 1
            sleep(0.01)
            if resp == 100:
                resp = 0
                trying_count += 1
                self.textBrowser.append('Trying to write zone ' + zone + '(' + str(trying_count) + '/5)')
                ser.flush()
                ser.write(('2E' + zone + data_to_write + '\n').encode())
                if emergency_stop == 500:
                    self.textBrowser.setStyleSheet('color: red')
                    self.textBrowser.append('Zone ' + zone + ' was NOT written!')
                    return

        resp = 0

        zones_write_count += 1
        self.write_progress.setValue(zones_write_count)
        if zone == '2901':
            self.textBrowser.append('Security zone was written!')
            self.textBrowser.append('Done!')
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
        send = Sender()
        if send.check_version() == 1:
            if self.connect_button:
                self.connect_button = False
                return
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
            self.connect_to_matrix_screen.setStyleSheet('color: green')
            self.connect_to_matrix_screen.setText('Connected to matrix screen!')
            self.connect_to_matrix_screen.setEnabled(False)
            self.info_label.setText('')
            self.connect_button = True
        elif send.check_version() == 0:
            if self.connect_button:
                self.connect_button = False
                return
            self.textBrowser.setEnabled(True)
            self.textBrowser.setStyleSheet('color: red')
            self.textBrowser.append('Your version of Display configurator is old! '
                                    'Please update it on <a href = "https://rupsa.ru/">https://rupsa.ru/</a>')
            self.connect_button = True
        else:
            if self.connect_button:
                self.connect_button = False
                return
            self.textBrowser.setEnabled(True)
            self.textBrowser.setStyleSheet('color: red')
            self.textBrowser.append('Unlocking of display is not success!'
                                    ' Your internet connection is too slow, or server is down. Try again later.')
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
        global data_0200
        global data_0400
        global data_0500
        global data_0600
        global data_2100
        global zones_write_count
        global zones_progress_bar_len

        self.write_progress.setValue(0)
        if self.zone_0200_write.isChecked():
            zones_progress_bar_len += 1
        if self.zone_0400_write.isChecked():
            zones_progress_bar_len += 1
        if self.zone_0500_write.isChecked():
            zones_progress_bar_len += 1
        if self.zone_0600_write.isChecked():
            zones_progress_bar_len += 1
        if self.zone_2100_write.isChecked():
            zones_progress_bar_len += 1
        # print(zones_progress_bar_len)
        self.write_progress.setMaximum(zones_progress_bar_len)

        data_0200 = self.zone_0201.text().replace(' ', '').replace('\r', '').replace('\n', '')
        data_0400 = self.zone_0401.text().replace(' ', '').replace('\r', '').replace('\n', '')
        data_0500 = self.zone_0501.text().replace(' ', '').replace('\r', '').replace('\n', '')
        data_0600 = self.zone_0601.text().replace(' ', '').replace('\r', '').replace('\n', '')
        data_2100 = self.zone_2101.text().replace(' ', '').replace('\r', '').replace('\n', '')

        send = Sender()
        send_and_write = send.send_data(rf080=hw_info, rf0fe=sw_info, r0200=zone_0200_read, r0400=zone_0400_read,
                                        r0500=zone_0500_read,
                                        r0600=zone_0600_read, r2100=zone_2100_read, w0200=data_0200, w0400=data_0400,
                                        w0500=data_0500,
                                        w0600=data_0600, w2100=data_2100)
        if send_and_write == 1:
            self.textBrowser.setStyleSheet('color: green')
            self.textBrowser.append('Connected to server!')

            self.unlock_display()
            self.textBrowser.append('Display unlocked')
            ser.flush()
            sleep(1)
            self.textBrowser.append('Start writing')
            if self.zone_0200_write.isChecked():
                self.write_zone(zone='0200', data_to_write=data_0200)
            if self.zone_0400_write.isChecked():
                self.write_zone(zone='0400', data_to_write=data_0400)
            if self.zone_0500_write.isChecked():
                self.write_zone(zone='0500', data_to_write=data_0500)
            if self.zone_0600_write.isChecked():
                self.write_zone(zone='0600', data_to_write=data_0600)
            if self.zone_2100_write.isChecked():
                self.write_zone(zone='2100', data_to_write=data_2100)
            self.write_zone(zone='2901', data_to_write='FD000000010101')
            ser.write(('222901' + '\n').encode())

            zones_write_count = 0
            zones_progress_bar_len = 1
            self.connect_button = True

        elif send_and_write == 0:
            self.textBrowser.setStyleSheet('color: red')
            self.textBrowser.append('No internet connection! Check your internet settings!')
            self.connect_button = True
        else:
            self.textBrowser.setEnabled(True)
            self.textBrowser.setStyleSheet('color: red')
            self.textBrowser.append('Data not written! '
                                    'Your internet connection is too slow, or server is down. Try again later.')
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
        self.textBrowser.setText('')
        self.connect_button = True

    def on_clear_faults_clicked(self):
        # Clearing faults
        self.textBrowser.setStyleSheet('color: black')
        if self.connect_button:
            self.connect_button = False
            return
        self.fault_row.setText('')
        ser.flush()
        ser.write(('14FFFFFF' + '\n').encode())
        self.connect_button = True

    def on_read_faults_clicked(self):
        # Reading faults
        self.textBrowser.setStyleSheet('color: black')
        if self.connect_button:
            self.connect_button = False
            return
        self.fault_row.setText('')
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

    # def on_calculate_2100_button_clicked(self):
    #     if self.connect_button:
    #         self.connect_button = False
    #         return
    #     zone_2100_data = zone_2100_mem
    #     convert = Converter()
    #     bin_data_2100_0 = convert.converter_from_hex(zone_2100_data)[0]
    #     if bin_data_2100_0[0] == '0':
    #         self.cb_2100_00_0.setChecked(False)
    #     else:
    #         self.cb_2100_00_0.setChecked(True)
    #
    #     if bin_data_2100_0[1] == '0':
    #         self.cb_2100_00_1.setChecked(False)
    #     else:
    #         self.cb_2100_00_1.setChecked(True)
    #
    #     if bin_data_2100_0[2] == '0':
    #         self.cb_2100_00_2.setChecked(False)
    #     else:
    #         self.cb_2100_00_2.setChecked(True)
    #
    #     if bin_data_2100_0[3] == '0':
    #         self.cb_2100_00_3.setChecked(False)
    #     else:
    #         self.cb_2100_00_3.setChecked(True)
    #
    #     if bin_data_2100_0[4] == '0':
    #         self.cb_2100_00_4.setChecked(False)
    #     else:
    #         self.cb_2100_00_4.setChecked(True)
    #
    #     if bin_data_2100_0[5] == '0':
    #         self.cb_2100_00_5.setChecked(False)
    #     else:
    #         self.cb_2100_00_5.setChecked(True)
    #
    #     if bin_data_2100_0[6] == '0':
    #         self.cb_2100_00_6.setChecked(False)
    #     else:
    #         self.cb_2100_00_6.setChecked(True)
    #     if bin_data_2100_0[7] == '0':
    #         self.cb_2100_00_7.setChecked(False)
    #     else:
    #         self.cb_2100_00_7.setChecked(True)
    #     print(bin_data_2100_0)
    #     print(zone_2100_data)
    #     self.connect_button = True


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
