from PyQt5 import QtCore, QtGui, QtWidgets




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(414, 432)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 0, 400, 400))
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 400, 400))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.chat_display = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.chat_display.setReadOnly(True)  # Make the chat display read-only
        self.chat_display.setObjectName("chat_display")
        self.verticalLayout.addWidget(self.chat_display)
        self.chat_input = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.chat_input.setObjectName("chat_input")
        self.verticalLayout.addWidget(self.chat_input)
        self.sendButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.sendButton.setObjectName("sendButton")
        self.verticalLayout.addWidget(self.sendButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Chat"))
        self.sendButton.setText(_translate("MainWindow", "Send"))

    def get_message(self):
        """Handles sending a message when the 'Send' button is clicked."""
        message = self.chat_input.text()
        if message:
            self.chat_input.clear()  
            return message
    def add_to_chat_display(self, message):
            """Allow external files to add messages."""
            self.chat_display.append(message)
    def button_clicked():
        return True

