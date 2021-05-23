import sys
from msilib.schema import Dialog

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import*


### ==> SPLASH SCREEN
from ui_splash_screen import Ui_SplashScreen

## ==> GLOBALS
counter = 0


# application
'''class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
'''

class SplashScreen(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ####### UI INTERFACE CODES #####

        ##### REMOVING TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # ==> QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        ### SHOW ==> MAIN WINDOW
        self.show()
        ### ==> END

    ## ==> APP FUNCTIONS
    ###########################################
    def progress(self):
        global counter
        # SETTING VALUE TO PROGRASS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASHSCREEN AND OPENING APP
        if counter > 45:
            # STOP TIMER
            self.timer.stop()

            # Close Splash Screen
            self.close()
        # increase counter
        counter += 1



app = QApplication(sys.argv)
qDialog = SplashScreen()
widget = QtWidgets.QStackedWidget()
widget.setFixedWidth(862)
widget.setFixedHeight(575)
app.exec_()

import main
main.Login()
exec('main')
app.exec_()