#!/usr/bin/env python

import rospy
from geographic_msgs.msg import GeoPointStamped

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPlainTextEdit, QPushButton
from PyQt5.QtCore import QSize    

import datetime

class NoteWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        rospy.init_node('geonote')
        self.positionSubscriber = rospy.Subscriber('/udp/position', GeoPointStamped, self.PositionCallback)

        self.setMinimumSize(QSize(640, 100))    
        self.setWindowTitle("Event Log") 

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)  

        self.positionLabel = QLabel("position", self)
        self.timeLabel = QLabel("time", self)

        lineEdit = QPlainTextEdit(self)
        logButton = QPushButton('log!',self)
        
        #title = QLabel("Hello World from PyQt", self) 
        #title.setAlignment(QtCore.Qt.AlignCenter) 
        #gridLayout.addWidget(title, 0, 0)
        
        gridLayout.addWidget(self.positionLabel, 0, 0)
        gridLayout.addWidget(self.timeLabel, 0, 1)
        gridLayout.addWidget(lineEdit, 1, 0)
        gridLayout.addWidget(logButton, 1, 1)

    def PositionCallback(self, data):
        #print data
        self.positionLabel.setText(str(data.position.latitude)+','+str(data.position.longitude))
        ts = datetime.datetime.utcfromtimestamp(data.header.stamp.secs)
        self.timeLabel.setText(ts.isoformat())
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = NoteWindow()
    mainWin.show()
    sys.exit( app.exec_() )
