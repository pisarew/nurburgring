import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize, Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sqlite3 as sq
from pyqtgraph.Qt import QtCore, QtGui
#from graph import CustomViewBox, CustomTickSliderItem
import numpy as np
import time


def time(name):
    with sq.connect("cars.db") as con:
        cur = sq.Cursor(con)
        cur.execute(f"SELECT * FROM cars WHERE pilot = '{name}'")
        result = cur.fetchall()
        
        time = [0] * len(result)
        j = 0
        for i in result:
            time[j] = round(timeCalculate(i[4]), 2)
            j += 1
        return time

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
    with sq.connect("cars.db") as con:
        cur = sq.Cursor(con)
        cur.execute(f"SELECT * FROM cars WHERE pilot = '{name}'")
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
        # grid = QtWidgets.QGridLayout(self)
        # grid.addWidget(self.widgetGraph, 0, 0)
        # self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])


        app = pg.mkQApp()

        axis = pg.DateAxisItem(orientation='bottom')
        vb = CustomViewBox()
    
        pw = pg.PlotWidget(viewBox=vb, axisItems={'bottom': axis}, enableMenu=False, title="PlotItem")

        

        dates = date(pilotName)
        dates.sort()
        # dates[1] += 100000000

        
        yArr = time(pilotName)
        print(dates)
        print(yArr)
        
        pw.plot(x = dates, y = yArr, symbol = 'o')

        # Using allowAdd and allowRemove to limit user interaction
        tickViewer = CustomTickSliderItem(allowAdd=False, allowRemove=False)
        vb.sigXRangeChanged.connect(tickViewer.updateRange)
        pw.plotItem.layout.addItem(tickViewer, 4, 1)

        # tickViewer.setTicks( [dates[0], dates[2], dates[-1]] )

        # pw.show()
        # pw.setWindowTitle('pyqtgraph example: customPlot')

       

        r = pg.PolyLineROI([(5,5), (10, 10)])
        pw.addItem(r)
        grid = QtWidgets.QVBoxLayout(self)
        grid.addWidget(self.label)
        grid.addWidget(pw)
        # self.widgetGraph = pw

    



    # def plot(self, hour, temperature): ## Построение графика
    #     self.widgetGraph.plot(hour, temperature)
        
    # def plot(self, name):
        # with sq.connect("cars.db") as con:
        #     cur = sq.Cursor(con)
        #     cur.execute("SELECT * WHERE pilot = '{name}'")
        #     result = cur.fetchall()
        #     deta = [''] * len(result)
        #     time = [''] * len(result)
        #     for i in result:


def timeCalculate(time):
    x = float(time[0]) + ((float(time[2:4]) * 10) / 600)
    return x


app = QApplication(sys.argv)
mainwindow = table()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(mainwindow)

mainwindow.show()

app.exec_()