import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize, Qt
import sqlite3 as sq


def addData(table):
    with sq.connect("cars.db") as con:
        cur = sq.Cursor(con)
        button1 = QtWidgets.QPushButton(table.centralwidget)

        button1.setObjectName('button1')
        button1.setText('mutton1')
        

        # pilotButton = [button1] * 38
        # cur.execute("SELECT pilot FROM pilots;")
        # pilots = cur.fetchall()
        # j = 0
        # for i in pilotButton:
        #     i.setText(pilots[j][0])
        #     j += 1

        

        
        cur.execute("SELECT * FROM cars;")
        cars = cur.fetchall()

        pilotButton = [button1] * len(cars)
        for i in range(len(cars)):
            pilotButton[i] = QtWidgets.QPushButton(table.centralwidget)

        table.tableWidget.setRowCount(len(cars))
        for i in range(len(cars)):
            table.tableWidget.setItem(i, 0, QTableWidgetItem(cars[i][0]))
            # table.tableWidget.setItem(i, 1, QTableWidgetItem(cars[i][1]))

            # cur.execute(f"SELECT id FROM pilots WHERE pilot = '{cars[i][1]}'")
            # if cur.fetchone() is not None:
            #     cur.execute(f"SELECT id FROM pilots WHERE pilot = '{cars[i][1]}'")
            #     j = cur.fetchone()[0]
            #     table.tableWidget.setCellWidget(i, 1, pilotButton[j])
            # else:
            #     table.tableWidget.setItem(i, 1, QTableWidgetItem('Водителя нет'))

            table.tableWidget.setCellWidget(i, 1, pilotButton[i])
            pilotButton[i].setText(cars[i][1])

            table.tableWidget.setItem(i, 2, QTableWidgetItem(cars[i][2]))
            table.tableWidget.setItem(i, 3, QTableWidgetItem(cars[i][3]))
            table.tableWidget.setItem(i, 4, QTableWidgetItem(cars[i][4]))
            table.tableWidget.setItem(i, 5, QTableWidgetItem(cars[i][5]))
            table.tableWidget.resizeColumnsToContents()
        return pilotButton

class table(QMainWindow):
    def __init__(self, parent = None):
        super(table, self).__init__(parent)
        loadUi("table.ui", self)
        self.tableWidget.setColumnCount(6)
        #self.tableWidget.setStretchLastSection(True)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setHorizontalHeaderLabels(["car", "pilot", "front", "back", "time", "date"])
        
        
        #Всплывающие подсказки
        self.tableWidget.horizontalHeaderItem(0).setToolTip("Магина")  
        
        j = 0
        for i in addData(self):
            j += 1
            i.clicked.connect(self.pilotClick)
    
    def pilotClick(self): #Сробатывает когда нажимаем на пилота
        sender = self.sender()
        print(sender.text() + ' was pressed')
        pilotWindow = pilotStat(sender.text())
        pilotWindow.show()
        pilotWindow.exec_()

class pilotStat(QDialog, table): #Окно пилота
    def __init__(self, pilotName):
        QDialog.__init__(self)
        loadUi("pilot.ui", self)
        self.label.setText(pilotName)



app = QApplication(sys.argv)
mainwindow = table()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(mainwindow)

mainwindow.show()

app.exec_()