import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from test import log_in, reg, user, cesh, casino

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.adminbutton.clicked.connect(self.admin)
   
    def loginfunction(self):
        username = self.username.text()
        password = self.password.text()
        if user(username):
            if log_in(username, password):
                print("Вхождение успешно!")
                Play = PlayCasino(username)
                widget.addWidget(Play)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                print("Неверный логин или паролоь")

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def admin(self):
        admintable = AdminTable()
        widget.addWidget(admintable)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("create.ui", self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.backButton.clicked.connect(self.back)
    
    def createaccfunction(self):
        username = self.username.text()
        if (self.password.text() == self.confirmpassword.text()) and (self.password.text() != '') and (self.username.text() != '') and (user(username) == False):
            password = self.password.text()
            reg(username, password)
            print("Аккаунт создан!\n", username, "\n", password)
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def back(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class PlayCasino(QDialog):
    username = ''
    def __init__(self, user_name):
        self.username = user_name
        super(PlayCasino, self).__init__()
        loadUi("play.ui", self)
        self.label_2.setText("Вы вошли как " + self.username)
        self.label_3.setText("Баланс - " + str(cesh(self.username)))
        self.Slider.setMinimum(500)
        self.Slider.setMaximum(100000)
        self.Slider.setValue(1000)
        self.Slider.setTickInterval(200)
        self.label_4.setText("ставка " + str(self.Slider.value()))
        self.Slider.valueChanged.connect(self.slider)
        self.playbutton.clicked.connect(self.playfunction)
        self.exitButton.clicked.connect(self.exit)
    def slider(self):
        self.label_4.setText("ставка " + str(self.Slider.value()))
    def playfunction(self):
        win = casino(self.username, self.Slider.value())
        if win == -1:
            self.label_4.setText("Вы лох!")
            self.label_3.setText("Баланс - " + str(cesh(self.username)))
        else:
            self.label_4.setText("Вы выиграли " + str(win) + '!!!')
            self.label_3.setText("Баланс - " + str(cesh(self.username)))
    
    def exit(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class AdminTable(QDialog):
    def __init__(self):
        super(AdminTable, self).__init__()
        loadUi("admintable.ui", self)
        self.usersTable.setColumnCount(3)
        self.usersTable.setRowCount(4)



app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(480)
widget.show()

app.exec_()

