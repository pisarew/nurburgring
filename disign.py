import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize, Qt
import sqlite3 as sq

def addData(table):
    with sq.connect("cars.db") as con:
        cur = sq.Cursor(con)
        cur.execute("SELECT * FROM cars;")
        cars = cur.fetchall()
        table.tableWidget.setRowCount(len(cars))
        for i in range(len(cars)):
            table.tableWidget.setItem(i, 0, QTableWidgetItem(cars[i][0]))
            table.tableWidget.setItem(i, 1, QTableWidgetItem(cars[i][1]))
            table.tableWidget.setItem(i, 2, QTableWidgetItem(cars[i][2]))
            table.tableWidget.setItem(i, 3, QTableWidgetItem(cars[i][3]))
            table.tableWidget.setItem(i, 4, QTableWidgetItem(cars[i][4]))
            table.tableWidget.setItem(i, 5, QTableWidgetItem(cars[i][5]))
            table.tableWidget.resizeColumnsToContents()

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
        addData(self)

        #Какая то херь
        # self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        # self.tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        # self.tableWidget.horizontalHeaderItem(5).setTextAlignment(Qt.AlignRight)




app = QApplication(sys.argv)
mainwindow = table()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(mainwindow)

mainwindow.show()

app.exec_()