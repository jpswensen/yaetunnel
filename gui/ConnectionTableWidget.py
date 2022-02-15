import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ConnectionTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super().__init__(1,5)

        self.setHorizontalHeaderLabels(list('ABCD'))
        self.setColumnWidth(4,200)
        #self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(250)

    def populate(self):
        
        #Row count 
        #self.setRowCount(6)  
  
        #Column count 
        self.setColumnCount(6)   
  
        #Table will fit the screen horizontally 
        self.setHorizontalHeaderLabels(('Device','Destination Port','Local Port','Available?','Tunnel','Launch'))
        self.horizontalHeader().setStretchLastSection(True) 
        self.horizontalHeader().setSectionResizeMode( 
            QHeaderView.Stretch) 

        self.horizontalHeader().setDefaultSectionSize(160)
        self.horizontalHeader().show()

    def _addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount)
 
    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)
