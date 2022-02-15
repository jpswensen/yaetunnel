# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import json
import subprocess
import os

import ConnectionTableWidget

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

class YAETunnelGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi("mainwindow.ui",self)   
        except:
            uic.loadUi("gui/mainwindow.ui",self)   
        
        self.tableWidget.populate()

        # k = '1'
        # v = "hello"
        # self.tableWidget._addRow()
        # self.tableWidget.setItem(0,0,QTableWidgetItem(k))
        # self.tableWidget.setItem(0,1,QTableWidgetItem(v))

        delegate = AlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.tableWidget.setItemDelegateForColumn(1, delegate)
        self.tableWidget.setItemDelegateForColumn(2, delegate)
        self.tableWidget.setItemDelegateForColumn(3, delegate)
        self.tableWidget.setItemDelegateForColumn(4, delegate)

        self.update_connection_table()

    def on_tunnel_button(self, row):
        name = row['name']
        port = row['dest_port']
        cmd = ['yaetunnel', 'connect', '--name' , f'{name}', '--port', f'{port}', 'pi']
        print(cmd)

        proc=subprocess.Popen(cmd,shell=False,stdout=None, stderr=None)
        zz=subprocess.list2cmdline(proc.args)
        print(zz)
        

    def on_launch_button(self, row):

        name = row['name']
        port = row['dest_port']
        cmd = f'yaetunnel connect --name={name} --port={port} --newterm pi'
        print(cmd)
        os.system(cmd)    
    
    def update_connection_table(self):
        cmd = ['yaetunnel', 'list', '--raw']
        py2output = subprocess.check_output(cmd, encoding='UTF-8')
        py2output = py2output.replace("'",'"')
        self.results = json.loads(py2output.strip())
        for K,V in enumerate(self.results):
            print(V['dest_port'])
            self.tableWidget._addRow()
            self.tableWidget.setItem(K,0,QTableWidgetItem(V['name']))
            self.tableWidget.setItem(K,1,QTableWidgetItem(str(V['dest_port'])))
            self.tableWidget.setItem(K,2,QTableWidgetItem(str(V['tun_port'])))
            self.tableWidget.setItem(K,3,QTableWidgetItem(str(V['connected'])))

            btn = QtWidgets.QPushButton('Open')
            self.tableWidget.setCellWidget(K,4, btn)
            btn.clicked.connect(lambda x, v=V: self.on_tunnel_button(v))

            btn = QtWidgets.QPushButton('Launch')
            self.tableWidget.setCellWidget(K,5, btn)
            btn.clicked.connect(lambda x, v=V: self.on_launch_button(v))
            
        



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = YAETunnelGUI()
    window.show()

    sys.exit(app.exec_())
