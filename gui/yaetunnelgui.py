# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import json
import subprocess

import ConnectionTableWidget




class YAETunnelGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi("mainwindow.ui",self)   
        except:
            uic.loadUi("gui/mainwindow.ui",self)   
        
        self.tableWidget.populate()

        k = '1'
        v = "hello"
        self.tableWidget._addRow()
        self.tableWidget.setItem(0,0,QTableWidgetItem(k))
        self.tableWidget.setItem(0,1,QTableWidgetItem(v))

        self.update_connection_table()
    
    def update_connection_table(self):
        cmd = ['yaetunnel', 'list', '--raw']
        py2output = subprocess.check_output(cmd, encoding='UTF-8')
        py2output = py2output.replace("'",'"')
        results = json.loads(py2output.strip())
        for K,V in enumerate(results):
            print(V['dest_port'])
            self.tableWidget._addRow()
            self.tableWidget.setItem(K,0,QTableWidgetItem(V['name']))
            self.tableWidget.setItem(K,1,QTableWidgetItem(str(V['dest_port'])))
            self.tableWidget.setItem(K,2,QTableWidgetItem(str(V['tun_port'])))
            self.tableWidget.setItem(K,3,QTableWidgetItem(str(V['connected'])))
        



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = YAETunnelGUI()
    window.show()

    sys.exit(app.exec_())
