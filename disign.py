import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize, Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sqlite3 as sq
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from createdb import parsingandcreate
import threading
import time



def pilotTime(name):
    with sq.connect("nurburgring.db") as con:
        cur = sq.Cursor(con)
        cur.execute(f"SELECT * FROM main WHERE pilot = '{name}'")
        result = cur.fetchall()
        
        timed = [0] * len(result)
        j = 0
        for i in result:
            timed[j] = round(timeCalculate(i[4]), 2)
            j += 1
        return timed

def dateConvertor(st):
    if st.lower() == 'январь' or st.lower() == 'января':
        return '01'
    elif st.lower() == 'февраль' or st.lower() == 'февраля':
        return '02'
    elif st.lower() == 'март' or st.lower() == 'марта':
        return '03'
    elif st.lower() == 'апрель' or st.lower() == 'апреля':
        return '04'
    elif st.lower() == 'май' or st.lower() == 'мая':
        return '05'
    elif st.lower() == 'июнь' or st.lower() == 'июня':
        return '06'
    elif st.lower() == 'июля' or st.lower() == 'июля':
        return '07'
    elif st.lower() == 'август' or st.lower() == 'августа':
        return '08'
    elif st.lower() == 'сентябрь' or st.lower() == 'сентября':
        return '09'
    elif st.lower() == 'октябрь' or st.lower() == 'октября':
        return '10'
    elif st.lower() == 'ноябрь' or st.lower() == 'ноября':
        return '11'
    elif st.lower() == 'декабрь' or st.lower() == 'декабря':
        return '12'
    else:
        return '09'

def date(name):
    with sq.connect("nurburgring.db") as con:
        cur = sq.Cursor(con)
        cur.execute(f"SELECT * FROM main WHERE pilot = '{name}'")
        cars = cur.fetchall()
        result = [0] * len(cars)
        j = 0
        for i in cars:
            if i[5] == '':
                result[j] = 946080000
            elif len(i[5].strip().split(" ")) == 1:
                result[j] = (int(i[5]) - 1970) * 31536000
            elif len(i[5].strip().split(" ")) == 2:
                # dateConvertor(i[5][0: i[5].find(" ")])
               result[j] = (int(i[5][i[5].find(" "):]) - 1970) * 31536000
            elif len(i[5].strip().split(" ")) == 3:
                result[j] = (int(i[5][i[5].rfind(" "):]) - 1970) * 31536000
            j += 1
        return result


def bestTime(name):
    with sq.connect("nurburgring.db") as con:
        cur = sq.Cursor(con)
        cur.execute(f"SELECT time FROM main WHERE pilot = '{name}'")
        cars = cur.fetchone()
        return cars[0]

def sumRecords(name):
    with sq.connect("nurburgring.db") as con:
        cur = sq.Cursor(con)
        cur.execute(f"SELECT records FROM pilots WHERE pilot = '{name}'")
        cars = cur.fetchone()
        return cars[0]

def addData(table):
    with sq.connect("nurburgring.db") as con:
        cur = sq.Cursor(con)
        button1 = QtWidgets.QPushButton(table.centralwidget)

        button1.setObjectName('button1')
        font = QtGui.QFont()
        font.setPointSize(12)
        button1.setFont(font)
        button1.setText('mutton1')
        cur.execute("SELECT * FROM main;")
        cars = cur.fetchall()

        pilotButton = [button1] * len(cars)
        button1.hide()
        for i in range(len(cars)):
            pilotButton[i] = QtWidgets.QPushButton(table.centralwidget)
            font = QtGui.QFont()
            font.setPointSize(12)
            pilotButton[i].setFont(font)
        table.tableWidget.setRowCount(len(cars))
        for i in range(len(cars)):
            table.tableWidget.setItem(i, 0, QTableWidgetItem(cars[i][0]))
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
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.addColumn)
        self.pushButton_3.clicked.connect(self.loadData)
        self.pushButton_4.clicked.connect(self.delete)
        
        
        #Всплывающие подсказки
        self.tableWidget.horizontalHeaderItem(0).setToolTip("Магина")  
        
        j = 0
        for i in addData(self):
            j += 1
            i.clicked.connect(self.pilotClick)
    
    def search(self):
        window = searchWindow()
        window.show()
        window.exec_()

    def pilotClick(self): #Сробатывает когда нажимаем на пилота
        sender = self.sender()
        print(sender.text() + ' was pressed')
        pilotWindow = pilotStat(sender.text())
        pilotWindow.show()
        pilotWindow.exec_()
    
    def addColumn(self):
        Window = addWindow()
        Window.show()
        Window.exec_()

    def delete(self):
        with sq.connect("nurburgring.db") as con:
            cur = sq.Cursor(con)
            cur.execute("DROP TABLE main;")
            con.commit()
            cur.execute("DROP TABLE pilots;")
            con.commit()
            cur.execute("DROP TABLE cars;")
            con.commit()
            cur.execute("""CREATE TABLE IF NOT EXISTS main (
                car TEXT,
                pilot TEXT,
                front TEXT,
                back TEXT,
                time TEXT,
                date TEXT
                )""")
            con.commit()
            cur.execute("""CREATE TABLE IF NOT EXISTS pilots (
                pilot TEXT,
                records INTEGER,
                id INTEGER
                )""")
            
            con.commit()

            cur.execute("""CREATE TABLE IF NOT EXISTS cars (
            brand TEXT,
            model TEXT,
            time INTEGER,
            date TEXT
            )""")
        
            con.commit()
            addData(self)

    def loadData(self):
        def parsingStart():
            parsingandcreate(Window)
            Window.hide()
        Window = loadingWindow()
        Window.show()
        t = threading.Thread(target=parsingStart)
        t.start()
        Window.exec_()
        
        j = 0
        for i in addData(self):
            j += 1
            i.clicked.connect(self.pilotClick)
        

class searchWindow(QDialog, table):
    def __init__(self):
        QDialog.__init__(self)
        loadUi("search.ui", self)
        self.comboBox.addItem("Автомобиль")
        self.comboBox.addItem("Пилот")
        self.comboBox.addItem("Шины")
        self.comboBox.addItem("Время круга")
        self.comboBox.addItem("Дата")
        self.accepted.connect(self.accept)
    def accept(self):
        searchText = self.lineEdit.text()
        searchCategori = self.comboBox.currentText()
        
        window = searchResult(searchCategori, searchText)
        window.show()
        window.exec_()


class searchResult(QDialog, table):
    def __init__(self, categori, text):
        QDialog.__init__(self)
        loadUi("searchResult.ui", self)
        with sq.connect("nurburgring.db") as con:
            cur = sq.Cursor(con)

            if categori == 'Автомобиль':
                cur.execute(f"SELECT * FROM main WHERE car = '{text}'")
            elif categori == 'Пилот':
                cur.execute(f"SELECT * FROM main WHERE pilot = '{text}'")
            elif categori == 'Шины':
                cur.execute(f"SELECT * FROM main WHERE back = '{text}'")
            elif categori == 'Время круга':
                cur.execute(f"SELECT * FROM main WHERE time = '{text}'")
            elif categori == 'Дата':
                cur.execute(f"SELECT * FROM main WHERE date = '{text}'")

            table = cur.fetchall()
            print(table)
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setRowCount(len(table))
            self.tableWidget.setSortingEnabled(True)
            self.tableWidget.setHorizontalHeaderLabels(["car", "pilot", "front", "back", "time", "date"])
            for i in range(len(table)):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(table[i][0]))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(table[i][1]))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(table[i][2]))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(table[i][3]))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(table[i][4]))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(table[i][5]))
            self.tableWidget.resizeColumnsToContents()

class loadingWindow(QDialog, table):
    def __init__(self):
        QDialog.__init__(self)
        loadUi("loading.ui", self)
        n = 160
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(n)
        self.progressBar.setValue(0)

        

#класс спизженый из документации pyqtgraph
class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        kwds['enableMenu'] = False
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)
        
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()
    
    ## reimplement mouseDragEvent to disable continuous axis zoom
    def mouseDragEvent(self, ev, axis=None):
        if axis is not None and ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev, axis=axis)
#второй класс спизженый из документации pyqtgraph
class CustomTickSliderItem(pg.TickSliderItem):
    def __init__(self, *args, **kwds):
        pg.TickSliderItem.__init__(self, *args, **kwds)
        
        self.all_ticks = {}
        self._range = [0,1]
    
    def setTicks(self, ticks):
        for tick, pos in self.listTicks():
            self.removeTick(tick)
        
        for pos in ticks:
            tickItem = self.addTick(pos, movable=False, color="#333333")
            self.all_ticks[pos] = tickItem
        
        self.updateRange(None, self._range)
    
    def updateRange(self, vb, viewRange):
        origin = self.tickSize/2.
        length = self.length

        lengthIncludingPadding = length + self.tickSize + 2
        
        self._range = viewRange
        
        for pos in self.all_ticks:
            tickValueIncludingPadding = (pos - viewRange[0]) / (viewRange[1] - viewRange[0])
            tickValue = (tickValueIncludingPadding*lengthIncludingPadding - origin) / length
            
            # Convert from np.bool_ to bool for setVisible
            visible = bool(tickValue >= 0 and tickValue <= 1)
            
            tick = self.all_ticks[pos]
            tick.setVisible(visible)

            if visible:
                self.setTickValue(tick, tickValue)


class pilotStat(QDialog, table): #Окно пилота
    def __init__(self, pilotName):
        QDialog.__init__(self)
        loadUi("pilot.ui", self)
        self.label.setText(pilotName)

        app = pg.mkQApp()

        axis = pg.DateAxisItem(orientation='bottom')
        vb = CustomViewBox()
    
        pw = pg.PlotWidget(viewBox=vb, axisItems={'bottom': axis}, enableMenu=False, title="PlotItem")

        

        dates = date(pilotName)
        dates.sort()

        
        yArr = pilotTime(pilotName)
        print(dates)
        print(yArr)
        
        pw.plot(x = dates, y = yArr, symbol = 'o')

        # Using allowAdd and allowRemove to limit user interaction
        tickViewer = CustomTickSliderItem(allowAdd=False, allowRemove=False)
        vb.sigXRangeChanged.connect(tickViewer.updateRange)
        pw.plotItem.layout.addItem(tickViewer, 4, 1)

        tickViewer.setTicks( [dates[0], dates[-1]] )

        # pw.show()
        # pw.setWindowTitle('pyqtgraph example: customPlot')

       
        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(self.label)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        grid.addWidget(pw)
        best = bestTime(pilotName)
        self.label_2.setText("Лучшее время: " + best)
        grid.addWidget(self.label_2)
        x = str(sumRecords(pilotName))
        self.label_3.setText("Количество рекордов: " + x)
        grid.addWidget(self.label_3)
        
        # self.widgetGraph = pw

class addWindow(QDialog, table):
    def __init__(self):
        QDialog.__init__(self)
        loadUi("addColumn.ui", self)
        self.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)   
    def accept(self):
        car = self.lineEdit.text()
        pilot = self.lineEdit_2.text()
        front = self.lineEdit_3.text()
        back = self.lineEdit_4.text()
        time = self.lineEdit_5.text()
        date = self.lineEdit_6.text()
        if car == '' or time == '' or not time[0].isdigit() or not time[2:4].isdigit():
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Не заполненны поля")
            error.show()
            error.exec_()
        else:
            if int(time[2:4]) > 59:
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setText("Недопустимое время!")
                error.show()
                error.exec_()
            else:
                with sq.connect("nurburgring.db") as con:
                    cur = sq.Cursor(con)
                    cur.execute(f"INSERT INTO main VALUES (?, ?, ?, ?, ?, ?)", (car, pilot, front, back, time, date))
                    con.commit()
                    cur.execute(f"SELECT * FROM pilots WHERE pilot = '{pilot}'")
                    if cur.fetchone() is None:
                        cur.execute(f"INSERT INTO pilots VALUES (?, ?, ?)", (pilot, 1, -1))
                j = 0
                for i in addData(mainwindow):
                    j += 1
                    i.clicked.connect(mainwindow.pilotClick)
                self.hide()




def timeCalculate(Time):
    x = float(Time[0]) + ((float(Time[2:4]) * 10) / 600)
    return x

with sq.connect("nurburgring.db") as con:
        cur = sq.Cursor(con)

        cur.execute("""CREATE TABLE IF NOT EXISTS main (
            car TEXT,
            pilot TEXT,
            front TEXT,
            back TEXT,
            time TEXT,
            date TEXT
        )""")
        con.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS pilots (
            pilot TEXT,
            records INTEGER,
            id INTEGER
            )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS cars (
            brand TEXT,
            model TEXT,
            time INTEGER,
            date TEXT
            )""")
        
        con.commit()


app = QApplication(sys.argv)
mainwindow = table()
mainwindow.show()

app.exec_()