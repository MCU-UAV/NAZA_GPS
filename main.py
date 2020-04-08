import sys
from MainWindows import *
from NazaGpsDecoder import  *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import serial.tools.list_ports
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

class MainForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.connectToCom)
        self.conState = False
        self.comList = []
        self.comListName = []
        self.initComList()
        self.timer = QTimer()
        self.timer.timeout.connect(self.time)
    def time(self):
        gpsInfo = self.decoder.readMessage("gps")['decoded']
        self.label_lat.setText("{:.07f}".format(gpsInfo['lat']))
        self.label_lon.setText("{:.07f}".format(gpsInfo['lon']))
        self.label_time.setText(str(gpsInfo['datetime']))
        self.label_satelites.setText((str(gpsInfo['satelites'])))
        self.label_gpsAlt.setText("{:.03f}".format(gpsInfo['gpsAlt']))
        self.label_fix.setText(str(gpsInfo['fix']))
        self.label_hdop.setText("{:.2f}".format(gpsInfo['hdop']))
        self.label_spd.setText("{:.2f}".format(gpsInfo['spd']))


    def initComList(self):
        tmp = serial.tools.list_ports.comports()
        for index in tmp:
            self.comList.append(index[0])
            self.comListName.append(index[1])
        self.comboBox.addItems(self.comListName)
        #print(list(serial.tools.list_ports.comports())[1][1])
        # print(self.comList)
        # print(self.comListName)
    def connectToCom(self):
        if self.conState is False:
            if self.comList != [] :
                try:
                    currentCom = self.comList[self.comListName.index(self.comboBox.currentText())]
                    self.decoder = NazaGpsDecoder(device=currentCom)
                    self.pushButton.setText('断开')
                    self.conState = True
                    self.label_sysmsg.setText("连接成功！")
                    self.timer.start(20)
                except Exception as e:
                    self.label_sysmsg.setText(str(e))
        else:
            self.pushButton.setText('连接')
            self.decoder.close()
            self.timer.stop()
            self.label_sysmsg.setText("等待连接！")
            self.conState = False
            self.label_lat.clear()
            self.label_lon.clear()
            self.label_time.clear()
            self.label_satelites.clear()
            self.label_gpsAlt.clear()
            self.label_fix.clear()
            self.label_hdop.clear()
            self.label_spd.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())