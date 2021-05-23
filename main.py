import sys
from msilib.schema import Dialog
from PyQt5 import QtGui
from PyQt5 import QtCore
import threading
import pymysql
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidgetItem, QTableWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
import os
import datetime

hostsFile_path = r"C:\Windows\System32\drivers\etc\hosts"
localhost = "127.0.0.1"

email = ""
lists = []
querylist = []
list_date = []


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.setWindowTitle("Login page")
        self.pixmap = QPixmap('aaa.jpg')

        # adding image to label
        self.label.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.label.setGeometry(QtCore.QRect(470, 10, 421, 561))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.button.clicked.connect(self.loginfunction)
        self.create.clicked.connect(self.gotocreate)

    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    def loginfunction(self):
        global email
        username = self.username.text()
        password = self.password.text()
        print("Successfully logged in with username: ", username, "and password:", password)
        # Made common database connection At top
        # conn = pymysql.connect(host="localhost", user="root", password="Mysql@06", db="Plannerfinal3")
        # cur = conn.cursor()
        query = "select name from user where Name=%s and Pswd=%s"

        conn = pymysql.connect(db="planner", user="root", password="Nark@1234", host="localhost", port=3306)
        cur = conn.cursor()
        cur.execute("select email from user where Name=%s and pswd=%s", (username, password))
        tup = cur.fetchone()
        email = ''.join(tup)
        cur.execute(query, (username, password))
        conn.commit()
        if len(cur.fetchall()) > 0:
            self.messagebox('login', 'Successful login!')
        else:
            self.messagebox('login', 'Invalid username or password!')
        # print("hi")

        # conn.close()
        datetime = code()
        widget.addWidget(datetime)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate(self):
        create = CreateAcc()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("create.ui", self)
        # self.email.clicked.connect(self.createfunction)
        self.setWindowTitle("Create page")
        self.label = QLabel(self)

        # loading image
        self.pixmap = QPixmap('imag.jpg')
        # adding image to label
        self.label.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.label.setGeometry(QtCore.QRect(550, 90, 441, 400))
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cpassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    def createaccfunction(self):
        mail = self.username_2.text()
        username = self.username.text()
        if self.password.text() == self.cpassword.text():
            password = self.password.text()
            print("Successfully created account with username : ", username, "and password: ", password)

            query = "insert into user values (%s,%s,%s)"
            # print(username)
            # print(password)
            db = pymysql.connect(db="planner", user="root", password="Nark@1234", host="localhost", port=3306)
            cur = db.cursor()
            query = "insert into user (email, Name, Pswd) values (%s,%s,%s)"
            data = cur.execute(query, (mail, username, password))
            # data = cur.execute("insert into user values (%s,%s,%s);"%(email, username, password))
            # data = cur.execute("insert into user values (%s,%s,%s)", ("email@email.com", "some", "1234"))
            # data = cur.execute("insert into user values (%s,%s,%s)", ("email1@email.com", "some1", "12345"))
            # print(data)
            if data:
                self.messagebox('SignUp', 'Successfully signed up!')
            else:
                self.messagebox('SignUp', 'Inappropriate password!')
            db.commit()
            db.close()
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class Dialog5(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Your Plan!"
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 400
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.creatingTables()
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.vBoxLayout)

        page = QWidget()
        page.proceed = QPushButton("Back ", page)
        page.proceed.setStyleSheet("background-color:rgb(44,44,44);")
        page.proceed.setStyleSheet("text-color:rgb(78, 234, 234);")

        page.grid = QGridLayout(page)
        page.grid.addWidget(page.proceed, 2, 2, 1, 1)
        page.proceed.clicked.connect(self.plan)
        # self.close()

        self.show()

    def plan(self):
        daypg = Day()
        widget.addWidget(daypg)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def creatingTables(self):
        self.tableWidget = QTableWidget()

        conn = pymysql.connect(db="planner", user="root", password="Nark@1234", host="localhost", port=3306)
        cur = conn.cursor()
        query6 = "select time.dates, planner.planname from time inner join planner on planner.plan_id = time.plan_id where email =%s"
        global list_date, plan
        cur.execute(query6, email)
        list_date = cur.fetchall()
        print(list_date)
        self.tableWidget.setRowCount(len(list_date) + 1)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Date"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Plan"))
        for i in range(len(list_date)):
            self.tableWidget.setItem(i + 1, 0,
                                     QTableWidgetItem(datetime.datetime.strftime(list_date[i][0], '%Y-%m-%d')))
            self.tableWidget.setItem(i + 1, 1, QTableWidgetItem(list_date[i][1]))

        conn.close()


class Day(QDialog):
    def __init__(self):
        super(Day, self).__init__()
        loadUi("day planner.ui", self)
        # self.addtask.textChanged.connect(self.save_text)
        self.clrtask.clicked.connect(self.save_text)
        self.view.clicked.connect(self.maintask)
        ###########################
        self.block.clicked.connect(self.blocksite)
        self.unblock.clicked.connect(self.unblocksite)
        self.addsite.toPlainText()
        self.hrs.clicked.connect(self.hours)
        self.logout.clicked.connect(self.logouts)
        ################
        self.addtask.clear()

    #########
    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    def blocksite(self):
        global sites
        sites = [self.addsite.toPlainText()]
        global x
        x = sites
        try:
            with open(hostsFile_path, "r+") as file:
                content = file.read()
                for site in sites:
                    if site in content:
                        pass
                    else:
                        file.write("\n" + localhost + " " + site)
                    self.messagebox('Info', 'all sites are blocked')
                # delay=int(input("ENter to delay:"))
                # start_time = threading.Timer(delay, self.unblocksite)
                # start_time.start()
                # print("End of the code")
        except:
            self.messagebox('Exception', 'error')

    def unblocksite(self):
        try:

            with open(hostsFile_path, "r+") as file:
                contents = file.readlines()
                file.seek(0)
                for content in contents:
                    if not any(website in content for website in sites):
                        file.write(content)
                file.truncate()
                self.messagebox('UNBLOCK', 'Done!')
        except:
            self.messagebox('Exception', 'error')


    #################
    def hours(self):
        timeinfo = int(self.time.toPlainText())
        # timer = QtCore.QTimer()
        # timer.timeout.connect(self.unblocknobutton())
        # timer.start(timeinfo)
        start_time = threading.Timer(timeinfo, self.unblocknobutton)
        start_time.start()

    def unblocknobutton(self):
        try:
            with open(hostsFile_path, "r+") as file:
                x = file.readlines()
                file.seek(0)
                for content in x:
                    if not any(website in content for website in sites):
                        file.write(content)
                file.truncate()
                print("Hi")
                # self.messagebox('UNBLOCK', 'Done!')
        except:
            self.messagebox('Exception', 'error')

    ###############
    def save_text(self):
        text = self.addtask.toPlainText()
        conn = pymysql.connect(db="planner", user="root", password="Nark@1234", host="localhost", port=3306)
        cur = conn.cursor()
        query4 = "insert into planner(planname) values (%s)"
        cur.execute(query4, text)
        conn.commit()
        # conn = pymysql.connect(db="planner", user="root", password="Nark@1234", host="localhost", port=3306)
        # cur = conn.cursor()
        query5 = "select plan_id from planner where planname =%s"
        cur.execute(query5, text)
        planid = cur.fetchone()
        conn.commit()
        # conn = pymysql.connect(db="planner", user="root", password="Nark@1234", host="localhost", port=3306)    cur = conn.cursor()
        for i in lists:
            query6 = "update time set plan_id= %s where dates=%s"
            cur.execute(query6, (planid, i))
            conn.commit()
        conn.close()

    def maintask(self):
        view = Dialog5()
        widget.addWidget(view)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logouts(self):
        loginpgs = Login()
        widget.addWidget(loginpgs)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Dialog1(QWidget):

    def __init__(self):
        # print(main.email)
        super().__init__()
        self.left, self.top, self.width, self.height = 200, 80, 862, 575

        self.page1 = self.create_page1()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.page1)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.stack)
        self.setLayout(hbox)

        self.show_page1()

        self.show()

    def create_page1(self):
        page = QWidget()

        page.calendar = QCalendarWidget(page)
        page.calendar.setStyleSheet("background-color: rgb(93,93,139);")
        # page.calendar.setStyleSheet("color:rgb(78, 234, 234);")
        page.calendar.setGridVisible(True)
        page.calendar.selectionChanged.connect(self.onSelectionChanged)  # onselectbutton

        page.label = QLabel(page)
        # page.label.setFont(QtGui.QFont("Sanserif", 10))
        page.label.setStyleSheet('color: rgb(44, 44, 44);')

        page.proceedbutton = QPushButton("Start planning ", page)

        page.proceedbutton.setStyleSheet("background-color:rgb(44,44,44);")
        page.proceedbutton.setStyleSheet("text-color:rgb(78, 234, 234);")
        # page.proceedbutton.setGeometry(QtCore.QRect(90, 370, 311, 71))
        page.proceedbutton.setToolTip("<h3>go ahead</h3>")
        page.proceedbutton.setEnabled(False)
        page.proceedbutton.clicked.connect(self.planner)  # planner

        page.backbutton = QPushButton("Back", page)
        page.backbutton.setStyleSheet("background-color:rgb(44,44,44);")
        page.backbutton.setStyleSheet("text-color:rgb(78, 234, 234);")
        page.backbutton.setToolTip("<h3>To main page</h3>")
        page.backbutton.clicked.connect(self.main)
        self.close()

        page.comboBox = None

        page.grid = QGridLayout(page)
        page.grid.addWidget(page.calendar, 0, 0, 1, 3)
        page.grid.addWidget(page.label, 1, 0, 1, 3)
        page.grid.addWidget(page.backbutton, 2, 1, 1, 1)
        page.grid.addWidget(page.proceedbutton, 2, 2, 1, 1)

        return page

    def show_page1(self):
        self.setWindowTitle("Select date from calendar")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.stack.setCurrentIndex(0)

    def onSelectionChanged(self):
        ca = self.page1.calendar.selectedDate()
        conn = pymysql.connect(db="planner", user="root", password="Nark@1234", host="localhost", port=3306)
        cur = conn.cursor()
        # QCalendarWidget.dateTextFormat
        # start_date = self.ui.calendarWidget_start_date_2.selectedDate().toString()
        # print data in text browser
        self.page1.label.setText(ca.toString("yyyy-MM-dd"))
        datew = ca.toString("yyyy-MM-dd")
        query2 = "insert into time(email,dates) values (%s,%s)"
        print(datew)
        cur.execute(query2, (email, datew))
        global lists
        lists.append(datew)
        ex = cur.fetchone()
        conn.commit()

        # print(ex)
        self.page1.proceedbutton.setEnabled(True)

    def planner(self):
        daypg = Day()
        widget.addWidget(daypg)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        # exec('planner')
        # os.system('python planner.py')

    def main(self):
        datetime = code()
        widget.addWidget(datetime)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        # os.system('python planner.py')


class code(QDialog):
    def __init__(self):
        super(code, self).__init__()
        loadUi('datetime.ui', self)
        self.Returns = 0
        self.SHOW.clicked.connect(self.onClicked)
        self.planner.clicked.connect(self.calender)
        self.reload.clicked.connect(self.onreload)
        self.text.setText("You may delay, but time will not.")

    @pyqtSlot()
    def onClicked(self):
        DateTime = datetime.datetime.now()
        self.DATE.setText('Date: %s-%s-%s' % (DateTime.day, DateTime.month, DateTime.year))
        self.TIME.setText('Time: %s:%s:%s' % (DateTime.hour, DateTime.minute, DateTime.second))

    @pyqtSlot()
    def onreload(self):
        self.text.setText("A man who dares to waste one hour of life has not discovered the value of life")
        self.reload.clicked.connect(self.onreloadagain)

    def onreloadagain(self):
        self.text.setText("It’s not that we have little time, but more that we waste a good deal of it")

    def calender(self):
        demo = Dialog1()
        widget.addWidget(demo)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        # import demo
        # demo.Dialog1()
        # exec('demo')
        # os.system('python demo.py')


app = QApplication(sys.argv)
loginpg = Login()
createpg = CreateAcc()
datetimepg = code()
daypgs = Day()
cod = code()

widget = QtWidgets.QStackedWidget()
widget.addWidget(loginpg)
widget.setFixedWidth(900)
widget.setFixedHeight(575)
widget.show()
app.exec_()
sys.exit(app.exec())
