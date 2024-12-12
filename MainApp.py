 # main.py

# -- coding: utf-8 --

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QMessageBox, QScrollArea, QLineEdit, QPushButton, QTextEdit, QProgressBar, QLabel, QFrame, QGridLayout, QSpinBox
)
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

from PyQt5.QtCore import pyqtSignal, Qt
import json
import socket
import sys
import resources_rc

global usernameA_
usernameA_ = ["None"]

import client, client_helper, database, server, server_helper, json, socket
from NotificationWindow import NotificationWindow

DEFAULT_IP = "localhost"
DEFAULT_PORT = 8080
BUFFER_SIZE = 4096
global client_socket

# Initialize and connect the socket
client_socket = client.connect_to_server()


def send_data(data):
     """
     Sends JSON-encoded data to the server and returns the server's response.

     Parameters:
         data (dict): The data to send to the server.

     Returns:
         dict: The JSON-decoded response from the server.
     """
     DEFAULT_IP = "localhost"
     DEFAULT_PORT = 8080
     BUFFER_SIZE = 4096

     try:
         # Send JSON-encoded data
         print("Data being sent: ",data,"---------------------")
         client_socket.sendall(json.dumps(data).encode('utf-8'))

         # Receive response
         response = client_socket.recv(BUFFER_SIZE).decode()
         received_data = json.loads(response)
         print("Data received",received_data,"---------------------")
         return received_data

     except socket.error as e:
         print(f"Connection error: {e}")
         QMessageBox.critical(None, "Connection Error", f"Unable to connect to server: {e}")
         return {"status": "error", "message": "Connection failed"}
     except json.JSONDecodeError as e:
         print(f"Invalid response from server: {e}")
         QMessageBox.critical(None, "Response Error", f"Invalid response from server.")
         return {"status": "error", "message": "Invalid server response"}





class Ui_WelcomePage(object):


    def setupUi(self, Widget):
        Widget.setObjectName("WelcomePage")
        Widget.setStyleSheet("background-color: #FF6F61;")  # Soft Coral Color

        self.main_layout = QVBoxLayout(Widget)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.main_layout.setSpacing(30)

        # Title Label
        self.label_2 = QLabel(Widget)
        self.label_2.setText("AUBoutique")
        self.label_2.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setFamily("Snap ITC")
        font.setPointSize(36)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.label_2)

        # Buttons Layout
        self.button_layout = QVBoxLayout()
        self.button_layout.setSpacing(20)
        self.button_layout.setAlignment(Qt.AlignHCenter)

        # Login Button
        self.pushButton = QPushButton("1- Login", Widget)
        self.pushButton.setFixedHeight(50)
        self.pushButton.setMinimumWidth(200)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #FF6F61;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFD1C1;
            }
        """)
        self.button_layout.addWidget(self.pushButton)

        # Register Button
        self.pushButton_2 = QPushButton("2- Register", Widget)
        self.pushButton_2.setFixedHeight(50)
        self.pushButton_2.setMinimumWidth(200)
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #FF6F61;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFD1C1;
            }
        """)
        self.button_layout.addWidget(self.pushButton_2)

        self.main_layout.addLayout(self.button_layout)

    def retranslateUi(self, Widget):
         _translate = QtCore.QCoreApplication.translate
         Widget.setWindowTitle(_translate("WelcomePage", "AUBOUTIQUE"))
         self.label_2.setText(_translate("WelcomePage",
                                         "<html><head/><body><p><span style=\" color:white;\">AUBoutique</span></p></body></html>"))
         self.pushButton.setText(_translate("WelcomePage", "1- Login"))
         self.pushButton_2.setText(_translate("WelcomePage", "2- Register"))


class Ui_MainMenuPage(object):
     def setupUi(self, Widget):
         Widget.setObjectName("MainMenuPage")
         Widget.resize(1100, 700)
         Widget.setStyleSheet("background-color: rgb(245, 250, 254);")

         self.gridLayout = QtWidgets.QGridLayout(Widget)
         self.gridLayout.setContentsMargins(0, 0, 0, 0)
         self.gridLayout.setSpacing(0)
         self.gridLayout.setObjectName("gridLayout")

         # ==============================
         # Sidebar (Icon Only Widget)
         # ==============================
         self.icon_only_widget = QtWidgets.QWidget(Widget)
         self.icon_only_widget.setStyleSheet("""
           QWidget{
               background-color: rgb(31,149,239);
           }
           QPushButton{
               color: white;
               height:40px;
               border:none;
               border-radius:10px;
               margin:5px;
           }
           QPushButton:checked{
               background-color: #F5FAFE;
               color:#1F95EF;
               font-weight:bold;
           }""")
         self.icon_only_widget.setObjectName("icon_only_widget")

         self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
         self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
         self.verticalLayout_3.setSpacing(5)
         self.verticalLayout_3.setObjectName("verticalLayout_3")

         # Profile Icon at the top of the sidebar
         self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
         self.horizontalLayout_3.setObjectName("horizontalLayout_3")
         self.label_4 = QtWidgets.QLabel(self.icon_only_widget)
         self.label_4.setMinimumSize(QtCore.QSize(40, 40))
         self.label_4.setMaximumSize(QtCore.QSize(40, 40))
         self.label_4.setText("")
         self.label_4.setPixmap(QtGui.QPixmap(":/Image/profile_white.png"))
         self.label_4.setScaledContents(True)
         self.label_4.setObjectName("label_4")
         self.horizontalLayout_3.addWidget(self.label_4, 0, Qt.AlignHCenter)
         self.verticalLayout_3.addLayout(self.horizontalLayout_3)

         # Load icons
         icon = QtGui.QIcon()
         icon.addPixmap(QtGui.QPixmap(":/Image/dashboard_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         icon1 = QtGui.QIcon()
         icon1.addPixmap(QtGui.QPixmap(":/Image/profile_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         icon2 = QtGui.QIcon()
         icon2.addPixmap(QtGui.QPixmap(":/Image/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         icon3 = QtGui.QIcon()
         icon3.addPixmap(QtGui.QPixmap(":/Image/cart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         icon4 = QtGui.QIcon()
         icon4.addPixmap(QtGui.QPixmap(":/Image/portfolio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         icon5 = QtGui.QIcon()
         icon5.addPixmap(QtGui.QPixmap(":/Image/funds.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         icon6 = QtGui.QIcon()
         icon6.addPixmap(QtGui.QPixmap(":/Image/messages_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         icon7 = QtGui.QIcon()
         icon7.addPixmap(QtGui.QPixmap(":/Image/log_out_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

         # Vertical Layout for Icon Buttons
         self.verticalLayout = QtWidgets.QVBoxLayout()
         self.verticalLayout.setContentsMargins(-1, 20, -1, -1)
         self.verticalLayout.setSpacing(15)
         self.verticalLayout.setAlignment(Qt.AlignTop)
         self.verticalLayout.setObjectName("verticalLayout")

         # Icon-only buttons
         self.view_products_1 = QtWidgets.QPushButton(self.icon_only_widget)
         self.view_products_1.setText("")
         self.view_products_1.setIcon(icon)
         self.view_products_1.setIconSize(QtCore.QSize(24, 24))
         self.view_products_1.setCheckable(True)
         self.view_products_1.setToolTip("View Products")
         self.verticalLayout.addWidget(self.view_products_1)

         self.view_owner_products1 = QtWidgets.QPushButton(self.icon_only_widget)
         self.view_owner_products1.setText("")
         self.view_owner_products1.setIcon(icon1)
         self.view_owner_products1.setIconSize(QtCore.QSize(24, 24))
         self.view_owner_products1.setCheckable(True)
         self.view_owner_products1.setToolTip("View Products by Owner")
         self.verticalLayout.addWidget(self.view_owner_products1)

         self.add_product1 = QtWidgets.QPushButton(self.icon_only_widget)
         self.add_product1.setText("")
         self.add_product1.setIcon(icon2)
         self.add_product1.setIconSize(QtCore.QSize(24, 24))
         self.add_product1.setCheckable(True)
         self.add_product1.setToolTip("Add Product")
         self.verticalLayout.addWidget(self.add_product1)

         self.buy_product1 = QtWidgets.QPushButton(self.icon_only_widget)
         self.buy_product1.setText("")
         self.buy_product1.setIcon(icon3)
         self.buy_product1.setIconSize(QtCore.QSize(24, 24))
         self.buy_product1.setCheckable(True)
         self.buy_product1.setToolTip("Buy Product")
         self.verticalLayout.addWidget(self.buy_product1)

         self.view_portfolio1 = QtWidgets.QPushButton(self.icon_only_widget)
         self.view_portfolio1.setText("")
         self.view_portfolio1.setIcon(icon4)
         self.view_portfolio1.setIconSize(QtCore.QSize(24, 24))
         self.view_portfolio1.setCheckable(True)
         self.view_portfolio1.setToolTip("View Portfolio")
         self.verticalLayout.addWidget(self.view_portfolio1)

         self.add_funds1 = QtWidgets.QPushButton(self.icon_only_widget)
         self.add_funds1.setText("")
         self.add_funds1.setIcon(icon5)
         self.add_funds1.setIconSize(QtCore.QSize(24, 24))
         self.add_funds1.setCheckable(True)
         self.add_funds1.setToolTip("Add Funds")
         self.verticalLayout.addWidget(self.add_funds1)

         self.text1 = QtWidgets.QPushButton(self.icon_only_widget)
         self.text1.setText("")
         self.text1.setIcon(icon6)
         self.text1.setIconSize(QtCore.QSize(24, 24))
         self.text1.setCheckable(True)
         self.text1.setToolTip("Chat")
         self.verticalLayout.addWidget(self.text1)

         self.verticalLayout_3.addLayout(self.verticalLayout)

         spacerItem = QtWidgets.QSpacerItem(20, 73, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
         self.verticalLayout_3.addItem(spacerItem)

         # Logout Button in Icon Sidebar
         self.pushButton_9 = QtWidgets.QPushButton(self.icon_only_widget)
         self.pushButton_9.setText("")
         self.pushButton_9.setIcon(icon7)
         self.pushButton_9.setIconSize(QtCore.QSize(24, 24))
         self.pushButton_9.setCheckable(True)
         self.pushButton_9.setToolTip("Logout")
         self.verticalLayout_3.addWidget(self.pushButton_9)

         self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)

         # ==============================
         # Larger Sidebar with Text
         # ==============================
         self.icon_name_widget = QtWidgets.QWidget(Widget)
         self.icon_name_widget.setStyleSheet("""
           QWidget{
               background-color: rgb(31,149,239);
               color: white;
           }
           QPushButton{
               color: white;
               text-align:left;
               height:40px;
               border:none;
               padding-left:15px;
               border-top-left-radius:10px;
               border-bottom-left-radius:10px;
               font-size: 14px;
           }
           QPushButton:checked{
               background-color: #F5FAFE;
               color:#1F95EF;
               font-weight:bold;
           }""")
         self.icon_name_widget.setObjectName("icon_name_widget")
         self.icon_name_widget.setMinimumWidth(0)
         self.icon_name_widget.setMaximumWidth(250)

         self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.icon_name_widget)
         self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
         self.verticalLayout_4.setSpacing(10)
         self.verticalLayout_4.setObjectName("verticalLayout_4")

         # Profile (Sidebar Expanded)
         self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
         self.horizontalLayout_2.setContentsMargins(-1, -1, 20, -1)
         self.horizontalLayout_2.setSpacing(10)
         self.horizontalLayout_2.setObjectName("horizontalLayout_2")

         self.label_2 = QtWidgets.QLabel(self.icon_name_widget)
         self.label_2.setMinimumSize(QtCore.QSize(40, 40))
         self.label_2.setMaximumSize(QtCore.QSize(40, 40))
         self.label_2.setText("")
         self.label_2.setPixmap(QtGui.QPixmap(":/Image/profile_white.png"))
         self.label_2.setScaledContents(True)
         self.label_2.setObjectName("label_2")
         self.horizontalLayout_2.addWidget(self.label_2)

         self.label_3 = QtWidgets.QLabel(self.icon_name_widget)
         font = QtGui.QFont()
         font.setPointSize(14)
         font.setBold(True)
         self.label_3.setFont(font)
         self.label_3.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
         self.label_3.setObjectName("label_3")
         self.horizontalLayout_2.addWidget(self.label_3)

         self.verticalLayout_4.addLayout(self.horizontalLayout_2)

         # Sidebar Buttons (Text + Icon)
         self.verticalLayout_2 = QtWidgets.QVBoxLayout()
         self.verticalLayout_2.setContentsMargins(-1, 20, -1, -1)
         self.verticalLayout_2.setSpacing(15)
         self.verticalLayout_2.setAlignment(Qt.AlignTop)

         self.view_products_2 = QtWidgets.QPushButton(self.icon_name_widget)
         self.view_products_2.setIcon(icon)
         self.view_products_2.setIconSize(QtCore.QSize(24, 24))
         self.view_products_2.setCheckable(True)
         self.view_products_2.setAutoExclusive(True)
         self.view_products_2.setToolTip("View Products")
         self.view_products_2.setText("View Products")
         self.verticalLayout_2.addWidget(self.view_products_2)

         self.view_owner_products2 = QtWidgets.QPushButton(self.icon_name_widget)
         self.view_owner_products2.setIcon(icon1)
         self.view_owner_products2.setIconSize(QtCore.QSize(24, 24))
         self.view_owner_products2.setCheckable(True)
         self.view_owner_products2.setAutoExclusive(True)
         self.view_owner_products2.setToolTip("View Products by Owner")
         self.view_owner_products2.setText("View Products by Owner")
         self.verticalLayout_2.addWidget(self.view_owner_products2)

         self.add_product2 = QtWidgets.QPushButton(self.icon_name_widget)
         self.add_product2.setIcon(icon2)
         self.add_product2.setIconSize(QtCore.QSize(24, 24))
         self.add_product2.setCheckable(True)
         self.add_product2.setAutoExclusive(True)
         self.add_product2.setToolTip("Add Product")
         self.add_product2.setText("Add Product")
         self.verticalLayout_2.addWidget(self.add_product2)

         self.buy_product2 = QtWidgets.QPushButton(self.icon_name_widget)
         self.buy_product2.setIcon(icon3)
         self.buy_product2.setIconSize(QtCore.QSize(24, 24))
         self.buy_product2.setCheckable(True)
         self.buy_product2.setAutoExclusive(True)
         self.buy_product2.setToolTip("Buy Product")
         self.buy_product2.setText("Buy Product")
         self.verticalLayout_2.addWidget(self.buy_product2)

         self.view_portfolio2 = QtWidgets.QPushButton(self.icon_name_widget)
         self.view_portfolio2.setIcon(icon4)
         self.view_portfolio2.setIconSize(QtCore.QSize(24, 24))
         self.view_portfolio2.setCheckable(True)
         self.view_portfolio2.setAutoExclusive(True)
         self.view_portfolio2.setToolTip("View Portfolio")
         self.view_portfolio2.setText("View Portfolio")
         self.verticalLayout_2.addWidget(self.view_portfolio2)

         self.add_funds2 = QtWidgets.QPushButton(self.icon_name_widget)
         self.add_funds2.setIcon(icon5)
         self.add_funds2.setIconSize(QtCore.QSize(24, 24))
         self.add_funds2.setCheckable(True)
         self.add_funds2.setAutoExclusive(True)
         self.add_funds2.setToolTip("Add Funds")
         self.add_funds2.setText("Add Funds")
         self.verticalLayout_2.addWidget(self.add_funds2)

         self.text2 = QtWidgets.QPushButton(self.icon_name_widget)
         self.text2.setIcon(icon6)
         self.text2.setIconSize(QtCore.QSize(24, 24))
         self.text2.setCheckable(True)
         self.text2.setAutoExclusive(True)
         self.text2.setToolTip("Chat")
         self.text2.setText("Chat")
         self.verticalLayout_2.addWidget(self.text2)

         self.verticalLayout_4.addLayout(self.verticalLayout_2)

         spacerItem1 = QtWidgets.QSpacerItem(20, 73, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
         self.verticalLayout_4.addItem(spacerItem1)

         self.pushButton_15 = QtWidgets.QPushButton(self.icon_name_widget)
         self.pushButton_15.setIcon(icon7)
         self.pushButton_15.setIconSize(QtCore.QSize(24, 24))
         self.pushButton_15.setCheckable(True)
         self.pushButton_15.setToolTip("Logout")
         self.pushButton_15.setText("Logout")
         self.verticalLayout_4.addWidget(self.pushButton_15)

         self.gridLayout.addWidget(self.icon_name_widget, 0, 1, 1, 1)

         # ==============================
         # Main Content Area
         # ==============================
         self.widget_3 = QtWidgets.QWidget(Widget)
         self.widget_3.setObjectName("widget_3")
         self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
         self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
         self.verticalLayout_5.setSpacing(10)
         self.verticalLayout_5.setObjectName("verticalLayout_5")

         # Header with Menu and Search
         self.widget = QtWidgets.QWidget(self.widget_3)
         self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
         self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
         self.horizontalLayout_4.setSpacing(10)

         # Menu Button
         self.menu = QtWidgets.QPushButton(self.widget)
         self.menu.setStyleSheet("border:none;")
         self.menu.setText("")
         icon8 = QtGui.QIcon()
         icon8.addPixmap(QtGui.QPixmap(":/Image/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         self.menu.setIcon(icon8)
         self.menu.setIconSize(QtCore.QSize(24, 24))
         self.menu.setCheckable(True)
         self.menu.setObjectName("menu")
         self.horizontalLayout_4.addWidget(self.menu)

         # Spacer
         self.horizontalLayout_4.addStretch()

         # Search Bar
         self.lineEdit = QtWidgets.QLineEdit(self.widget)
         self.lineEdit.setObjectName("lineEdit")
         self.lineEdit.setPlaceholderText("Search...")
         self.lineEdit.setFixedHeight(30)
         self.lineEdit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc; 
                border-radius: 5px; 
                padding: 0 8px; 
                font-size:14px;
            }
        """)
         self.horizontalLayout_4.addWidget(self.lineEdit)

         self.pushButton_21 = QtWidgets.QPushButton(self.widget)
         self.pushButton_21.setText("")
         icon9 = QtGui.QIcon()
         icon9.addPixmap(QtGui.QPixmap(":/Image/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         self.pushButton_21.setIcon(icon9)
         self.pushButton_21.setIconSize(QtCore.QSize(24, 24))
         self.pushButton_21.setObjectName("pushButton_21")
         self.pushButton_21.setStyleSheet("border:none;")
         self.pushButton_21.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.horizontalLayout_4.addWidget(self.pushButton_21)

         # Another Spacer
         self.horizontalLayout_4.addStretch()

         # Profile Button
         self.pushButton_20 = QtWidgets.QPushButton(self.widget)
         self.pushButton_20.setStyleSheet("border:none;")
         self.pushButton_20.setText("")
         icon10 = QtGui.QIcon()
         icon10.addPixmap(QtGui.QPixmap(":/Image/profile_black.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         self.pushButton_20.setIcon(icon10)
         self.pushButton_20.setIconSize(QtCore.QSize(24, 24))
         self.pushButton_20.setObjectName("pushButton_20")
         self.pushButton_20.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.horizontalLayout_4.addWidget(self.pushButton_20)

         self.verticalLayout_5.addWidget(self.widget)

         # Stacked Widget for Main Content Pages
         self.header_widget = QtWidgets.QStackedWidget(self.widget_3)
         self.header_widget.setStyleSheet("background-color: rgb(255, 255, 255);")
         self.header_widget.setObjectName("header_widget")

         # View Products Page (0)
         self.view_products_page = QtWidgets.QWidget()
         vlayout_products = QtWidgets.QVBoxLayout(self.view_products_page)
         vlayout_products.setContentsMargins(20, 20, 20, 20)
         vlayout_products.setSpacing(10)

         self.label = QtWidgets.QLabel("Products Menu", self.view_products_page)
         font = QtGui.QFont()
         font.setPointSize(20)
         font.setBold(True)
         self.label.setFont(font)
         self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
         self.label.setObjectName("label")
         vlayout_products.addWidget(self.label)

         self.scroll_area = QtWidgets.QScrollArea(self.view_products_page)
         self.scroll_area.setWidgetResizable(True)
         self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
         vlayout_products.addWidget(self.scroll_area)

         self.products_container = QtWidgets.QWidget()
         self.products_layout = QtWidgets.QGridLayout(self.products_container)
         self.products_layout.setContentsMargins(0, 0, 0, 0)
         self.products_layout.setSpacing(20)
         self.scroll_area.setWidget(self.products_container)
         self.header_widget.addWidget(self.view_products_page)

         # Owner Products Page (1)
         self.products_by_owner_page = QtWidgets.QWidget()
         self.vlayout_owner = QtWidgets.QVBoxLayout(self.products_by_owner_page)
         self.vlayout_owner.setContentsMargins(20, 20, 20, 20)
         self.vlayout_owner.setSpacing(10)

         self.top_owner_layout = QtWidgets.QHBoxLayout()
         self.top_owner_layout.setSpacing(10)

         self.go_to_chat_button = QtWidgets.QPushButton("Chat")
         self.go_to_chat_button.setFixedSize(60, 30)
         self.go_to_chat_button.setStyleSheet("""
               QPushButton {
                   background-color: #1F95EF;
                   color: white;
                   border-radius: 5px;
               }
               QPushButton:hover {
                   background-color: #166BB5;
               }
           """)
         self.go_to_chat_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.go_to_chat_button.clicked.connect(lambda: self.header_widget.setCurrentIndex(6))

         self.top_owner_layout.addWidget(self.go_to_chat_button, alignment=QtCore.Qt.AlignLeft)

         self.label_5 = QtWidgets.QLabel("Owner Products", self.products_by_owner_page)
         font = QtGui.QFont()
         font.setPointSize(20)
         font.setBold(True)
         self.label_5.setFont(font)
         self.label_5.setAlignment(QtCore.Qt.AlignCenter)
         self.label_5.setObjectName("label_5")

         self.top_owner_layout.addStretch()
         self.top_owner_layout.addWidget(self.label_5, alignment=QtCore.Qt.AlignCenter)
         self.top_owner_layout.addStretch()

         self.vlayout_owner.addLayout(self.top_owner_layout)

         self.scroll_area_owner = QtWidgets.QScrollArea(self.products_by_owner_page)
         self.scroll_area_owner.setWidgetResizable(True)
         self.scroll_area_owner.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
         self.vlayout_owner.addWidget(self.scroll_area_owner)

         self.owner_products_container = QtWidgets.QWidget()
         self.owner_products_layout = QtWidgets.QGridLayout(self.owner_products_container)
         self.owner_products_layout.setContentsMargins(0, 0, 0, 0)
         self.owner_products_layout.setSpacing(20)
         self.scroll_area_owner.setWidget(self.owner_products_container)
         self.header_widget.addWidget(self.products_by_owner_page)

         # Add Product Page (2)
         self.add_product_page = QtWidgets.QWidget()
         vlayout_add = QtWidgets.QVBoxLayout(self.add_product_page)
         vlayout_add.setContentsMargins(20, 20, 20, 20)
         vlayout_add.setSpacing(20)

         self.label_6 = QtWidgets.QLabel("Add Products", self.add_product_page)
         font = QtGui.QFont()
         font.setPointSize(20)
         font.setBold(True)
         self.label_6.setFont(font)
         self.label_6.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
         self.label_6.setObjectName("label_6")
         vlayout_add.addWidget(self.label_6)

         self.add_product_stack = QStackedWidget(self.add_product_page)
         self.add_product_stack.setStyleSheet("background-color: #FFFFFF;")

         # Form Page (A0)
         self.add_product_form_page = QtWidgets.QWidget()
         form_layout = QtWidgets.QVBoxLayout(self.add_product_form_page)
         form_layout.setContentsMargins(20, 20, 20, 20)
         form_layout.setSpacing(20)

         self.lineEdit_owner = QLineEdit(self.add_product_form_page)
         self.lineEdit_owner.setPlaceholderText("Owner (username)")
         self.lineEdit_name = QLineEdit(self.add_product_form_page)
         self.lineEdit_name.setPlaceholderText("Product Name")
         self.lineEdit_quantity = QLineEdit(self.add_product_form_page)
         self.lineEdit_quantity.setPlaceholderText("Quantity")
         self.lineEdit_price = QLineEdit(self.add_product_form_page)
         self.lineEdit_price.setPlaceholderText("Price")
         self.textEdit_description = QTextEdit(self.add_product_form_page)
         self.textEdit_description.setPlaceholderText("Description")

         form_layout.addWidget(self.lineEdit_owner)
         form_layout.addWidget(self.lineEdit_name)
         form_layout.addWidget(self.lineEdit_quantity)
         form_layout.addWidget(self.lineEdit_price)
         form_layout.addWidget(self.textEdit_description)

         self.add_product_progress_bar = QProgressBar(self.add_product_form_page)
         self.add_product_progress_bar.setMinimum(0)
         self.add_product_progress_bar.setMaximum(100)
         self.add_product_progress_bar.setValue(0)
         form_layout.addWidget(self.add_product_progress_bar)

         self.pushButton_submit_product = QPushButton("Add Product", self.add_product_form_page)
         self.pushButton_submit_product.setFixedHeight(40)
         self.pushButton_submit_product.setStyleSheet("""
                               QPushButton {
                                   background-color: #1F95EF; 
                                   color: white; 
                                   border-radius: 5px; 
                                   font-weight: bold;
                               }
                               QPushButton:hover {
                                   background-color: #166BB5;
                               }
                           """)
         self.pushButton_submit_product.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         form_layout.addWidget(self.pushButton_submit_product, alignment=QtCore.Qt.AlignHCenter)

         self.add_product_stack.addWidget(self.add_product_form_page)

         # Success Page (A1)
         self.success_page = QtWidgets.QWidget()
         success_layout = QtWidgets.QVBoxLayout(self.success_page)
         success_layout.setContentsMargins(20, 20, 20, 20)
         success_layout.setSpacing(20)
         self.success_label = QLabel("Product added successfully!", self.success_page)
         font_s = QtGui.QFont()
         font_s.setPointSize(16)
         font_s.setBold(True)
         self.success_label.setFont(font_s)
         self.success_label.setAlignment(QtCore.Qt.AlignCenter)
         success_layout.addWidget(self.success_label)

         self.back_button_success = QPushButton("Back", self.success_page)
         self.back_button_success.setFixedHeight(30)
         self.back_button_success.setStyleSheet("""
                       QPushButton {
                           background-color: #1F95EF; 
                           color: white; 
                           border-radius: 5px; 
                           font-weight: bold;
                       }
                       QPushButton:hover {
                           background-color: #166BB5;
                       }
                   """)
         self.back_button_success.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         success_layout.addWidget(self.back_button_success, alignment=QtCore.Qt.AlignHCenter)

         self.add_product_stack.addWidget(self.success_page)

         # Error Page (A2)
         self.error_page = QtWidgets.QWidget()
         error_layout = QtWidgets.QVBoxLayout(self.error_page)
         error_layout.setContentsMargins(20, 20, 20, 20)
         error_layout.setSpacing(20)
         self.error_label = QLabel("Error: Please fill all fields correctly!", self.error_page)
         self.error_label.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")
         self.error_label.setAlignment(QtCore.Qt.AlignCenter)
         error_layout.addWidget(self.error_label)

         self.back_button_error = QPushButton("Back", self.error_page)
         self.back_button_error.setFixedHeight(30)
         self.back_button_error.setStyleSheet("""
                       QPushButton {
                           background-color: #1F95EF; 
                           color: white; 
                           border-radius: 5px; 
                           font-weight: bold;
                       }
                       QPushButton:hover {
                           background-color: #166BB5;
                       }
                   """)
         self.back_button_error.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         error_layout.addWidget(self.back_button_error, alignment=QtCore.Qt.AlignHCenter)

         self.add_product_stack.addWidget(self.error_page)

         self.add_product_stack.setCurrentIndex(0)
         vlayout_add.addWidget(self.add_product_stack)
         self.header_widget.addWidget(self.add_product_page)

         # Buy Product Page (3)
         self.buy_product_page = QtWidgets.QWidget()
         vlayout_buy = QtWidgets.QVBoxLayout(self.buy_product_page)
         vlayout_buy.setContentsMargins(20, 20, 20, 20)
         vlayout_buy.setSpacing(20)
         #Title of page
         self.label_7 = QtWidgets.QLabel("Buy Products", self.buy_product_page)
         font = QtGui.QFont()
         font.setPointSize(20)
         font.setBold(True)
         self.label_7.setFont(font)
         self.label_7.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
         self.label_7.setObjectName("label_7")
         vlayout_buy.addWidget(self.label_7)
          # vlayout_buy.addStretch() # now  no need i need to implement it
         # Finish button at top-left
         self.finish_button = QtWidgets.QPushButton("FINISH", self.buy_product_page)
         self.finish_button.setStyleSheet("""
                     QPushButton {
                         background-color: #1F95EF; 
                         color: white; 
                         border-radius: 5px; 
                         font-weight: bold;
                         font-size:16px;
                         padding:5px;
                     }
                     QPushButton:hover {
                         background-color: #166BB5;
                     }
                 """)
         self.finish_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.finish_button.clicked.connect(self.handle_finish_purchase)

         # Horizontal layout to place finish button on top-left
         top_buy_layout = QtWidgets.QHBoxLayout()
         top_buy_layout.addWidget(self.finish_button, 0, Qt.AlignLeft)
         top_buy_layout.addStretch()
         vlayout_buy.addLayout(top_buy_layout)

         # Scroll area for products
         self.buy_products_scroll = QtWidgets.QScrollArea(self.buy_product_page)
         self.buy_products_scroll.setWidgetResizable(True)
         vlayout_buy.addWidget(self.buy_products_scroll)

         self.buy_products_container = QtWidgets.QWidget()
         self.buy_products_layout = QtWidgets.QGridLayout(self.buy_products_container)
         self.buy_products_layout.setContentsMargins(0, 0, 0, 0)
         self.buy_products_layout.setSpacing(20)
         self.buy_products_scroll.setWidget(self.buy_products_container)

         # Quantity SpinBox for selecting how many units to buy
         h_layout_qty = QtWidgets.QHBoxLayout()
         self.quantity_spin = QtWidgets.QSpinBox(self.buy_product_page)
         self.quantity_spin.setMinimum(1)
         self.quantity_spin.setValue(1)
         h_layout_qty.addWidget(QtWidgets.QLabel("Quantity to Purchase:"))
         h_layout_qty.addWidget(self.quantity_spin)
         vlayout_buy.addLayout(h_layout_qty)
         self.header_widget.addWidget(self.buy_product_page)

         # Portfolio Page (4) -
         self.view_portfolio_page = QtWidgets.QWidget()
         vlayout_portfolio = QtWidgets.QVBoxLayout(self.view_portfolio_page)
         vlayout_portfolio.setContentsMargins(20, 20, 20, 20)
         vlayout_portfolio.setSpacing(20)
         self.label_8 = QtWidgets.QLabel("Portfolio Page", self.view_portfolio_page)
         font = QtGui.QFont()
         font.setPointSize(20)
         font.setBold(True)
         self.label_8.setFont(font)
         self.label_8.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
         self.label_8.setObjectName("label_8")
         vlayout_portfolio.addWidget(self.label_8)
         #vlayout_portfolio.addStretch()# NO NEED FOR THAT NOWWW
         # In setupUi for portfolio page
         self.balance_label = QLabel(self.view_portfolio_page)
         self.balance_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
         vlayout_portfolio.addWidget(self.balance_label, 0, Qt.AlignLeft)

         # Owned products scroll area
         self.owned_products_scroll = QScrollArea(self.view_portfolio_page)
         self.owned_products_scroll.setWidgetResizable(True)
         self.owned_products_container = QWidget()
         self.owned_products_layout = QVBoxLayout(self.owned_products_container)
         self.owned_products_scroll.setWidget(self.owned_products_container)
         vlayout_portfolio.addWidget(QLabel("Owned Products:", self.view_portfolio_page))
         vlayout_portfolio.addWidget(self.owned_products_scroll)

         # Transactions scroll area
         self.transactions_scroll = QScrollArea(self.view_portfolio_page)
         self.transactions_scroll.setWidgetResizable(True)
         self.transactions_container = QWidget()
         self.transactions_layout = QVBoxLayout(self.transactions_container)
         self.transactions_scroll.setWidget(self.transactions_container)
         vlayout_portfolio.addWidget(QLabel("Transactions:", self.view_portfolio_page))
         vlayout_portfolio.addWidget(self.transactions_scroll)
         self.header_widget.addWidget(self.view_portfolio_page)

         # Add Funds Page (5)
         self.add_funds_page = QtWidgets.QWidget()
         vlayout_funds = QtWidgets.QVBoxLayout(self.add_funds_page)
         vlayout_funds.setContentsMargins(20, 20, 20, 20)
         vlayout_funds.setSpacing(20)
         self.label_9 = QtWidgets.QLabel("Add Funds", self.add_funds_page)
         font = QtGui.QFont()
         font.setPointSize(20)
         font.setBold(True)
         self.label_9.setFont(font)
         self.label_9.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
         self.label_9.setObjectName("label_9")
         vlayout_funds.addWidget(self.label_9)
         #vlayout_funds.addStretch()
         self.add_funds_stack = QStackedWidget(self.add_funds_page)
         vlayout_funds.addWidget(self.add_funds_stack)

         # Add Funds Form Page (F0)
         self.add_funds_form_page = QtWidgets.QWidget()
         aff_layout = QtWidgets.QVBoxLayout(self.add_funds_form_page)
         aff_layout.setContentsMargins(0, 0, 0, 0)
         aff_layout.setSpacing(30)

         # Big appealing entry
         self.funds_label = QLabel("Enter Amount to Add:", self.add_funds_form_page)
         self.funds_label.setAlignment(Qt.AlignCenter)
         self.funds_label.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
         aff_layout.addWidget(self.funds_label)

         self.funds_lineedit = QLineEdit(self.add_funds_form_page)
         self.funds_lineedit.setPlaceholderText("0.00")
         self.funds_lineedit.setAlignment(Qt.AlignCenter)
         self.funds_lineedit.setFixedWidth(300)
         self.funds_lineedit.setStyleSheet("""
                     QLineEdit {
                         background-color: #FFFFFF;
                         border:2px solid #1F95EF;
                         border-radius:10px;
                         font-size:20px;
                         padding:10px;
                     }
                 """)
         aff_layout.addWidget(self.funds_lineedit, 0, Qt.AlignCenter)

         # Animated appealing button (simple hover effect)
         self.funds_submit_button = QPushButton("Submit", self.add_funds_form_page)
         self.funds_submit_button.setFixedSize(200, 50)
         self.funds_submit_button.setStyleSheet("""
                     QPushButton {
                         background-color:#1F95EF; 
                         color:white; 
                         border-radius:5px; 
                         font-size:20px;font-weight:bold;
                     }
                     QPushButton:hover {
                         background-color:#166BB5;
                     }
                 """)
         self.funds_submit_button.clicked.connect(self.handle_add_funds)
         aff_layout.addWidget(self.funds_submit_button, 0, Qt.AlignCenter)

         self.add_funds_stack.addWidget(self.add_funds_form_page)

         # Add Funds Success Page (F1)
         self.add_funds_success_page = QWidget()
         afs_layout = QVBoxLayout(self.add_funds_success_page)
         afs_layout.setContentsMargins(20, 20, 20, 20)
         self.af_success_label = QLabel("Funds added successfully!", self.add_funds_success_page)
         self.af_success_label.setStyleSheet("color:green;font-size:20px;font-weight:bold;")
         self.af_success_label.setAlignment(Qt.AlignCenter)
         afs_layout.addWidget(self.af_success_label)
         self.back_button_add_funds_success = QPushButton("Back", self.add_funds_success_page)
         self.back_button_add_funds_success.setFixedHeight(30)
         self.back_button_add_funds_success.setStyleSheet("""
                QPushButton {
                    background-color: #1F95EF; 
                    color: white; 
                    border-radius: 5px; 
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #166BB5;
                }
            """)
         self.back_button_add_funds_success.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         afs_layout.addWidget(self.back_button_add_funds_success, alignment=QtCore.Qt.AlignHCenter)
         self.back_button_add_funds_success.clicked.connect(lambda: self.add_funds_stack.setCurrentIndex(0))
         self.add_funds_stack.addWidget(self.add_funds_success_page)

         # Add Funds Error Page (F2)
         self.add_funds_error_page = QWidget()
         afe_layout = QVBoxLayout(self.add_funds_error_page)
         afe_layout.setContentsMargins(20, 20, 20, 20)
         self.af_error_label = QLabel("Error adding funds!", self.add_funds_error_page)
         self.af_error_label.setStyleSheet("color:red;font-size:20px;font-weight:bold;")
         self.af_error_label.setAlignment(Qt.AlignCenter)
         afe_layout.addWidget(self.af_error_label)
         self.back_button_add_funds_error = QPushButton("Back", self.add_funds_error_page)
         self.back_button_add_funds_error.setFixedHeight(30)
         self.back_button_add_funds_error.setStyleSheet("""
                QPushButton {
                    background-color: #1F95EF; 
                    color: white; 
                    border-radius: 5px; 
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #166BB5;
                }
            """)
         self.back_button_add_funds_error.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         afe_layout.addWidget(self.back_button_add_funds_error, alignment=QtCore.Qt.AlignHCenter)
         self.back_button_add_funds_error.clicked.connect(lambda: self.add_funds_stack.setCurrentIndex(0))
         self.add_funds_stack.addWidget(self.add_funds_error_page)

         self.header_widget.addWidget(self.add_funds_page)



         # Chat Page (6)

         self.text_page = QtWidgets.QWidget()
         vlayout_text = QtWidgets.QVBoxLayout(self.text_page)
         vlayout_text.setContentsMargins(20, 20, 20, 20)
         vlayout_text.setSpacing(10)

         # Chat label
         self.label_10 = QtWidgets.QLabel("Chat", self.text_page)
         font = QtGui.QFont()
         font.setPointSize(20)
         self.label_10.setFont(font)
         self.label_10.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
         self.label_10.setObjectName("label_10")
         vlayout_text.addWidget(self.label_10)

         self.header_widget.addWidget(self.text_page)

         # Instantiate and add NotificationWindow
         self.notification_page = QtWidgets.QWidget()  
         notification_layout = QVBoxLayout(self.notification_page) 
         self.notification_window = NotificationWindow(usernameA_,client_socket)
         vlayout_text.addWidget(self.notification_window)

         # Add the notification page to the layout
         self.verticalLayout_5.addWidget(self.header_widget) 
         self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1) 

         # Add the notification page to the main widget layout
         self.verticalLayout_5.addWidget(self.notification_page)


         # Free Purchase Page (7)
         self.free_purchase_page = QtWidgets.QWidget()
         fp_layout = QtWidgets.QVBoxLayout(self.free_purchase_page)
         fp_layout.setContentsMargins(20, 20, 20, 20)
         fp_layout.setSpacing(20)
         fp_label = QLabel("Congratulations! You've earned a free purchase!", self.free_purchase_page)
         fp_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
         fp_label.setAlignment(Qt.AlignCenter)
         fp_layout.addWidget(fp_label)

         self.fp_button = QPushButton("Go to Buy Products", self.free_purchase_page)
         self.fp_button.setStyleSheet("""
            QPushButton {
                background-color: #1F95EF;
                color: white;
                border-radius:5px;
                font-weight:bold;
            }
            QPushButton:hover {
                background-color:#166BB5;
            }
        """)
         self.fp_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.fp_button.clicked.connect(lambda: self.header_widget.setCurrentIndex(3))  # buy products
         fp_layout.addWidget(self.fp_button, 0, Qt.AlignHCenter)
         self.header_widget.addWidget(self.free_purchase_page)

         # ==============================
         # Buy Result Pages (Success/Error)
         # ==============================
         # Index 8: Buy Success Page (Green)
         self.buy_success_page = QtWidgets.QWidget()
         buy_s_layout = QtWidgets.QVBoxLayout(self.buy_success_page)
         buy_s_layout.setContentsMargins(20, 20, 20, 20)
         self.buy_success_label = QtWidgets.QLabel("Thank you for your purchase!", self.buy_success_page)
         self.buy_success_label.setAlignment(Qt.AlignCenter)
         self.buy_success_label.setStyleSheet("color: green; font-size:20px; font-weight:bold;")
         buy_s_layout.addWidget(self.buy_success_label)
         self.back_button_buy_success = QPushButton("Back")
         self.back_button_buy_success.setFixedHeight(30)
         self.back_button_buy_success.setStyleSheet("""
                QPushButton {
                    background-color: #1F95EF; 
                    color: white; 
                    border-radius: 5px; 
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #166BB5;
                }
            """)
         self.back_button_buy_success.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         buy_s_layout.addWidget(self.back_button_buy_success, alignment=QtCore.Qt.AlignHCenter)
         self.back_button_buy_success.clicked.connect(lambda : self.header_widget.setCurrentIndex(3))
         self.header_widget.addWidget(self.buy_success_page)

         # Index 9: Buy Error Page (Red)
         self.buy_error_page = QtWidgets.QWidget()
         buy_e_layout = QtWidgets.QVBoxLayout(self.buy_error_page)
         buy_e_layout.setContentsMargins(20, 20, 20, 20)
         self.buy_error_label = QtWidgets.QLabel("Insufficient funds!", self.buy_error_page)
         self.buy_error_label.setAlignment(Qt.AlignCenter)
         self.buy_error_label.setStyleSheet("color: red; font-size:20px; font-weight:bold;")
         buy_e_layout.addWidget(self.buy_error_label)
         self.back_button_buy_error = QPushButton("Back")
         self.back_button_buy_error.setFixedHeight(30)
         self.back_button_buy_error.setStyleSheet("""
                QPushButton {
                    background-color: #1F95EF; 
                    color: white; 
                    border-radius: 5px; 
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #166BB5;
                }
            """)
         self.back_button_buy_error.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         buy_e_layout.addWidget(self.back_button_buy_error, alignment=QtCore.Qt.AlignHCenter)
         self.back_button_buy_error.clicked.connect(
             lambda: self.header_widget.setCurrentIndex(3))  # Go back to buy page
         self.header_widget.addWidget(self.buy_error_page)

         self.verticalLayout_5.addWidget(self.header_widget)
         self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1)

         # Hide the icon_name_widget initially
         self.icon_name_widget.hide()

         self.retranslateUi(Widget)

         # Initially show the first page
         self.header_widget.setCurrentIndex(0)

         # Connect menu button to toggle animation
         self.menu.toggled.connect(self.animate_side_bar)

         # Synchronize toggles
         self.text1.toggled['bool'].connect(self.text2.setChecked)
         self.add_funds1.toggled['bool'].connect(self.add_funds2.setChecked)
         self.view_portfolio1.toggled['bool'].connect(self.view_portfolio2.setChecked)
         self.buy_product1.toggled['bool'].connect(self.buy_product2.setChecked)
         self.add_product1.toggled['bool'].connect(self.add_product2.setChecked)
         self.view_owner_products1.toggled['bool'].connect(self.view_owner_products2.setChecked)
         self.view_products_1.toggled['bool'].connect(self.view_products_2.setChecked)
         self.view_products_2.toggled['bool'].connect(self.view_products_1.setChecked)
         self.view_owner_products2.toggled['bool'].connect(self.view_owner_products1.setChecked)
         self.add_product2.toggled['bool'].connect(self.add_product1.setChecked)
         self.buy_product2.toggled['bool'].connect(self.buy_product1.setChecked)
         self.view_portfolio2.toggled['bool'].connect(self.view_portfolio1.setChecked)
         self.add_funds2.toggled['bool'].connect(self.add_funds1.setChecked)
         self.text2.toggled['bool'].connect(self.text1.setChecked)

         # Instead of closing the entire window on logout, emit a logout_signal
         self.pushButton_9.clicked.connect(self.logout_signal.emit)
         self.pushButton_15.clicked.connect(self.logout_signal.emit)

         # Page navigation
         self.view_products_1.clicked.connect(lambda: self.header_widget.setCurrentIndex(0))
         self.view_products_2.clicked.connect(lambda: self.header_widget.setCurrentIndex(0))
         self.view_owner_products1.clicked.connect(lambda: self.show_all_owners_products())
         self.view_owner_products2.clicked.connect(lambda: self.show_all_owners_products())
         self.add_product1.clicked.connect(lambda: self.header_widget.setCurrentIndex(2))
         self.add_product2.clicked.connect(lambda: self.header_widget.setCurrentIndex(2))
         self.buy_product1.clicked.connect(lambda: self.show_buy_products_page())
         self.buy_product2.clicked.connect(lambda: self.show_buy_products_page())
         self.view_portfolio1.clicked.connect(lambda: self.header_widget.setCurrentIndex(4))
         self.view_portfolio2.clicked.connect(lambda: self.header_widget.setCurrentIndex(4))
         self.add_funds1.clicked.connect(lambda: self.header_widget.setCurrentIndex(5))
         self.add_funds2.clicked.connect(lambda: self.header_widget.setCurrentIndex(5))
         self.text1.clicked.connect(lambda: self.header_widget.setCurrentIndex(6))
         self.text2.clicked.connect(lambda: self.header_widget.setCurrentIndex(6))
         self.view_portfolio1.clicked.connect(lambda: (self.header_widget.setCurrentIndex(4), self.load_portfolio()))
         self.view_portfolio2.clicked.connect(lambda: (self.header_widget.setCurrentIndex(4), self.load_portfolio()))

         # Connect add product button
         self.pushButton_submit_product.clicked.connect(self.handle_add_product_submission)

         # Connect top search button
         self.pushButton_21.clicked.connect(self.search_products)

         self.add_product_progress = 0

         # Load all products
         self.load_all_products()

         # Connect back buttons
         self.back_button_error.clicked.connect(self.back_to_form_from_error)
         self.back_button_success.clicked.connect(self.back_to_form_from_success)

     def retranslateUi(self, Widget):
         _translate = QtCore.QCoreApplication.translate
         Widget.setWindowTitle(_translate("MainMenuPage", "AUBoutique"))
         self.label_3.setText(_translate("MainMenuPage", "Sidebar"))
         self.view_products_2.setText(_translate("MainMenuPage", "View Products"))
         self.view_owner_products2.setText(_translate("MainMenuPage", "View Products by Owner"))
         self.add_product2.setText(_translate("MainMenuPage", "Add Product"))
         self.buy_product2.setText(_translate("MainMenuPage", "Buy Product"))
         self.view_portfolio2.setText(_translate("MainMenuPage", "View Portfolio"))
         self.add_funds2.setText(_translate("MainMenuPage", "Add Funds"))
         self.text2.setText(_translate("MainMenuPage", "Chat"))
         self.pushButton_15.setText(_translate("MainMenuPage", "Logout"))
         self.label.setText(_translate("MainMenuPage", "Products Menu"))
         self.label_5.setText(_translate("MainMenuPage", "Owner Products"))
         self.label_6.setText(_translate("MainMenuPage", "Add Products"))
         self.label_7.setText(_translate("MainMenuPage", "Buy Products"))
         self.label_8.setText(_translate("MainMenuPage", "Portfolio Page"))
         self.label_9.setText(_translate("MainMenuPage", "Add Funds"))
         self.label_10.setText(_translate("MainMenuPage", "Chat"))

     def animate_side_bar(self, checked):
         self.icon_name_widget.show()
         self.animation = QPropertyAnimation(self.icon_name_widget, b"maximumWidth")
         self.animation.setDuration(300)
         self.animation.setEasingCurve(QEasingCurve.InOutCubic)
         if checked:
             self.animation.setStartValue(0)
             self.animation.setEndValue(250)
         else:
             self.animation.setStartValue(self.icon_name_widget.width())
             self.animation.setEndValue(0)
         self.animation.finished.connect(self.handle_animation_finished)
         self.animation.start()

     def handle_animation_finished(self):
         if self.icon_name_widget.maximumWidth() == 0:
             self.icon_name_widget.hide()

     def load_all_products(self):
         self.all_products = self.get_all_products_from_server()
         # debugging:
         print("Fetched products: ", self.all_products)
         # Filter out products with 0 quantity
         self.all_products = [p for p in self.all_products if p.get('quantity', 0) > 0]
         self.display_products(self.all_products)

     def handle_add_product_submission(self):
         owner = self.lineEdit_owner.text().strip()
         name = self.lineEdit_name.text().strip()
         quantity_str = self.lineEdit_quantity.text().strip()
         price_str = self.lineEdit_price.text().strip()
         description = self.textEdit_description.toPlainText().strip()

         if not owner or not name or not price_str or not description or not quantity_str:
             self.error_label.setText("Error: Please fill all fields correctly!")
             self.add_product_stack.setCurrentIndex(2)  # error page
             return

         try:
             price = float(price_str)
             quantity = int(quantity_str)
             if price < 0 or quantity <= 0:
                 raise ValueError("Invalid values")
         except ValueError:
             self.error_label.setText("Error: Price must be a valid positive number and quantity must be > 0!")
             self.add_product_stack.setCurrentIndex(2)  # error page
             return

         add_data = {
             "action": "ADD_PRODUCT",
             "name": name,
             "price": price,
             "description": description,
             "owner": owner,
             "picture_path": "",
             "quantity": quantity
         }

         response = send_data(add_data)
         if response.get("status") == "success":
             self.success_label.setText("Product added successfully!")
             self.add_product_stack.setCurrentIndex(1)  # success page
             added_quantity = quantity
             self.add_product_progress += added_quantity * 10
             if self.add_product_progress >= 100:
                 self.add_product_progress = 100
                 self.add_product_progress_bar.setValue(self.add_product_progress)
                 # Show free purchase page
                 self.header_widget.setCurrentIndex(7)
             else:
                 self.add_product_progress_bar.setValue(self.add_product_progress)

             self.load_all_products()
         else:
             server_message = response.get("message", "Unknown error occurred.")
             self.error_label.setText(f"Error: {server_message}")
             self.add_product_stack.setCurrentIndex(2)  # error page

     def get_all_products_from_server(self):
         view_data = {"action": "VIEW_PRODUCTS"}
         response = send_data(view_data)
         products = response.get("products", [])
         return products

     def get_products_by_owner_from_server(self, owner_name):
         view_data = {
             "action": "VIEW_OWNER",
             "owner_name": owner_name,
             "product_id": None
         }
         response = send_data(view_data)
         owner_products = response.get("owner_products", {}).get(owner_name, [])
         # Filter out 0 quantity
         owner_products = [p for p in owner_products if p.get('quantity', 0) > 0]
         print("Owner products fetched: ", owner_products)
         return owner_products

     def get_all_owners_products_from_server(self):
         data = {"action": "VIEW_ALL_OWNERS"}
         response = send_data(data)
         print("VIEW_ALL_OWNERS response: ", response)
         owners_dict = response.get("owners", {})
         # Filter out 0 quantity products
         for o in owners_dict:
             owners_dict[o] = [p for p in owners_dict[o] if p.get('quantity', 0) > 0]
         return owners_dict

     def display_products(self, products, no_products_message="No products available"):
         # Clear layout
         for i in reversed(range(self.products_layout.count())):
             widget = self.products_layout.itemAt(i).widget()
             if widget:
                 widget.setParent(None)
         if not products:
             no_label = QtWidgets.QLabel(no_products_message)
             no_label.setAlignment(Qt.AlignCenter)
             self.products_layout.addWidget(no_label, 0, 0)
             return
         columns = 3
         for idx, product in enumerate(products):
             row = idx // columns
             col = idx % columns
             card = self.create_product_card(product, clickable_owner=True)
             self.products_layout.addWidget(card, row, col)

     def display_owner_products(self, products, owner_name, no_products_message=None):
         # Clear layout
         for i in reversed(range(self.owner_products_layout.count())):
             widget = self.owner_products_layout.itemAt(i).widget()
             if widget:
                 widget.setParent(None)

         self.label_5.setText(f"Products by {owner_name}")

         if not products:
             if no_products_message is None:
                 no_products_message = f"No products available by {owner_name}"
             no_label = QtWidgets.QLabel(no_products_message)
             no_label.setAlignment(Qt.AlignCenter)
             self.owner_products_layout.addWidget(no_label, 0, 0)
             return

         columns = 3
         for idx, product in enumerate(products):
             row = idx // columns
             col = idx % columns
             card = self.create_owner_product_card(product)
             self.owner_products_layout.addWidget(card, row, col)

     def display_all_owners_products(self, owners_dict):
         # Clear layout
         for i in reversed(range(self.owner_products_layout.count())):
             w = self.owner_products_layout.itemAt(i).widget()
             if w:
                 w.setParent(None)

         if not owners_dict:
             no_label = QLabel("No owners or products available")
             no_label.setAlignment(Qt.AlignCenter)
             self.owner_products_layout.addWidget(no_label, 0, 0)
             return

         row = 0
         for owner, products in owners_dict.items():
             owner_label = QLabel(f"<b>Owner:</b> {owner}")
             self.owner_products_layout.addWidget(owner_label, row, 0, 1, 3)
             row += 1
             if not products:
                 no_products_label = QLabel("No products for this owner")
                 self.owner_products_layout.addWidget(no_products_label, row, 0)
                 row += 1
             else:
                 for idx, product in enumerate(products):
                     col = idx % 3
                     if idx % 3 == 0 and idx != 0:
                         row += 1
                     card = self.create_owner_product_card(product)
                     self.owner_products_layout.addWidget(card, row, col)
                 row += 1

     def search_products(self):
         query = self.lineEdit.text().strip().lower()
         current_index = self.header_widget.currentIndex()
         print("Searching for: " ,query, "in index", current_index)
         if current_index == 0:
             # View products page search by product name
             if not query:
                 self.display_products(self.all_products)
                 return
             filtered = [p for p in self.all_products if
                         query in p.get("name", "").lower() and p.get('quantity', 0) > 0]
             if not filtered:
                 self.display_products([], no_products_message="Product not Found")
             else:
                 self.display_products(filtered)

         elif current_index == 1:
             # View owner products page search by owner name
             if not query:
                 # Show all owners
                 owners_dict = self.get_all_owners_products_from_server()
                 self.display_all_owners_products(owners_dict)
                 return
             owner_products = self.get_products_by_owner_from_server(query)
             if not owner_products:
                 self.display_owner_products([], query, no_products_message="No products found for this owner")
             else:
                 self.display_owner_products(owner_products, query)

     def create_product_card(self, product, clickable_owner=False):
         card_widget = QFrame()
         card_widget.setStyleSheet("QFrame{border:1px solid #ccc;border-radius:5px;background:#fff;}")

         layout = QVBoxLayout(card_widget)
         name_label = QLabel(f"<b>Name:</b> {product.get('name', 'N/A')}")
         price_label = QLabel(f"<b>Price:</b> {product.get('price', '0.00')}")
         quantity_label = QLabel(f"<b>Quantity:</b> {product.get('quantity', '0')}")

         # If clickable_owner True, make owner a button
         if clickable_owner:
             owner_button = QPushButton(f"Owner: {product.get('owner', 'N/A')}")
             owner_button.setStyleSheet("border:none; color: blue; text-decoration: underline;")
             owner_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
             owner_button.clicked.connect(lambda: self.show_owner_products(product.get('owner', 'N/A')))
             layout.addWidget(name_label)
             layout.addWidget(price_label)
             layout.addWidget(quantity_label)
             layout.addWidget(owner_button)
         else:
             owner_label = QLabel(f"<b>Owner:</b> {product.get('owner', 'N/A')}")
             layout.addWidget(name_label)
             layout.addWidget(price_label)
             layout.addWidget(quantity_label)
             layout.addWidget(owner_label)

         desc_label = QLabel(f"<b>Description:</b> {product.get('description', 'N/A')}")
         desc_label.setWordWrap(True)
         layout.addWidget(desc_label)
         return card_widget

     def create_owner_product_card(self, product):
         # This card will have a link to buy products page
         card_widget = QFrame()
         card_widget.setStyleSheet("QFrame{border:1px solid #ccc;border-radius:5px;background:#fff;}")

         layout = QVBoxLayout(card_widget)
         # Just show owner, product name, description
         name_label = QLabel(f"<b>Name:</b> {product.get('name', 'N/A')}")
         desc_label = QLabel(f"<b>Description:</b> {product.get('description', 'N/A')}")
         desc_label.setWordWrap(True)
         layout.addWidget(name_label)
         layout.addWidget(desc_label)

         # Link (button) to go to buy products page
         buy_button = QPushButton("Buy Now")
         buy_button.setStyleSheet("color:blue;text-decoration:underline;background:none;border:none;")
         buy_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         buy_button.clicked.connect(lambda: self.redirect_to_buy_products(product.get("product_id")))
         layout.addWidget(buy_button, alignment=Qt.AlignLeft)
         return card_widget

     def redirect_to_buy_products(self, product_id):
         self.header_widget.setCurrentIndex(3)
         self.display_buy_products(self.all_products)
         self.select_product_for_purchase(product_id)

     def show_owner_products(self, owner_name):
         print("Attempting to show owner products for: ", owner_name)
         self.header_widget.setCurrentIndex(1)
         owner_products = self.get_products_by_owner_from_server(owner_name)
         print("Owner products (After fetch): ", owner_products)
         self.display_owner_products(owner_products, owner_name)

     def show_all_owners_products(self):
         self.header_widget.setCurrentIndex(1)
         owners_dict = self.get_all_owners_products_from_server()
         self.display_all_owners_products(owners_dict)

     def back_to_form_from_error(self):
         self.add_product_stack.setCurrentIndex(0)
         self.reset_add_product_form()

     def back_to_form_from_success(self):
         self.add_product_stack.setCurrentIndex(0)
         self.reset_add_product_form()

     def reset_add_product_form(self):
         self.lineEdit_owner.clear()
         self.lineEdit_name.clear()
         self.lineEdit_price.clear()
         self.textEdit_description.clear()
         self.lineEdit_quantity.clear()
         self.add_product_progress_bar.setValue(self.add_product_progress)

     def show_buy_products_page(self):
         self.header_widget.setCurrentIndex(3)
         # Filter out products with quantity == 0
         products_for_buy = [p for p in self.all_products if p.get('quantity', 0) > 0]
         self.display_buy_products(products_for_buy)

     def display_buy_products(self, products):
         # Clear layout
         for i in reversed(range(self.buy_products_layout.count())):
             w = self.buy_products_layout.itemAt(i).widget()
             if w:
                 w.setParent(None)
         if not products:
             no_label = QLabel("No products available")
             no_label.setAlignment(Qt.AlignCenter)
             self.buy_products_layout.addWidget(no_label, 0, 0)
             return

         columns = 3
         for idx, product in enumerate(products):
             row = idx // columns
             col = idx % columns
             card = self.create_product_card(product, clickable_owner=False)
             # clicking card selects product
             product_id = product.get("product_id")
             card.mousePressEvent = lambda event, pid=product_id: self.select_product_for_purchase(pid)
             self.buy_products_layout.addWidget(card, row, col)

     def select_product_for_purchase(self, product_id):
         # Store selected product_id for later use in handle_finish_purchase
         self.selected_product_id = product_id
         QMessageBox.information(None, "Selected", f"Selected product ID {product_id} for purchase.")
         # On actual purchase confirm, we should reset progress if it's a free purchase scenario handled by server.

     def handle_finish_purchase(self):
         if not  self.current_user_id:
             QMessageBox.warning(None, "Error", "No username available. Please log in.")
             return
         if not hasattr(self, "selected_product_id"):
             QMessageBox.warning(None, "No Selection", "Please select a product first.")
             return
         quantity = self.quantity_spin.value()
         free_purchase = (self.add_product_progress == 100)  # If progress at 100, this purchase is free.

         data = {
             "action": "BUY_PRODUCTS",
             "user_id": self.current_user_id,
             "product_id": self.selected_product_id,
             "quantity": quantity,
             "free_purchase": free_purchase
         }
         response = send_data(data)
         if response.get("status") == "success":
             # Purchase successful
             # If it was a free purchase, reset progress bar
             if free_purchase:
                 self.add_product_progress = 0
                 self.add_product_progress_bar.setValue(0)
             self.load_all_products()
             # Show success page
             self.header_widget.setCurrentIndex(8)
         else:
             # Error during purchase
             msg = response.get("message", "Error during purchase")
             if "Insufficient" in msg:
                 self.buy_error_label.setText(msg)
                 self.buy_error_label.setStyleSheet("color:red;font-size:20px;font-weight:bold;")
                 self.header_widget.setCurrentIndex(9)
             else:
                 # Generic error also show on error page
                 self.buy_error_label.setText(msg)
                 self.header_widget.setCurrentIndex(9)

     def handle_add_funds(self):
         if not  self.current_user_id:
             QMessageBox.warning(None, "Error", "No username available. Please log in.")
             return
         amount_str = self.funds_lineedit.text().strip()
         if not amount_str:
             self.af_error_label.setText("Please enter an amount.")
             self.add_funds_stack.setCurrentIndex(2)  # error page
             return
         try:
             amount = float(amount_str)
             if amount <= 0:
                 raise ValueError()
         except ValueError:
             self.af_error_label.setText("Invalid amount.")
             self.add_funds_stack.setCurrentIndex(2)  # error page
             return

         data = {"action": "ADD_FUNDS", "user_id": self.current_user_id, "amount": amount}
         response = send_data(data)
         if response.get("status") == "success":
             # Show success page
             self.af_success_label.setText(f"Funds added successfully! New Balance: {response['new_balance']}")
             self.add_funds_stack.setCurrentIndex(1)
         else:
             self.af_error_label.setText(response.get("message", "An error occurred"))
             self.add_funds_stack.setCurrentIndex(2)

     def load_portfolio(self):
         if not  self.username:
             QMessageBox.warning(None, "Error", "No username available. Please log in.")
             return
         data = {"action": "VIEW_PORTFOLIO", "username": self.username}
         response = send_data(data)
         if response.get("status") == "success":
             balance = response.get("balance", 0.0)
             self.balance_label.setText(f"Balance: {balance}")

             # Clear owned products layout
             for i in reversed(range(self.owned_products_layout.count())):
                 w = self.owned_products_layout.itemAt(i).widget()
                 if w:
                     w.setParent(None)

             owned_products = response.get("owned_products", [])
             if not owned_products:
                 no_owned = QLabel("No owned products")
                 no_owned.setAlignment(Qt.AlignCenter)
                 self.owned_products_layout.addWidget(no_owned)
             else:
                 for p in owned_products:
                     p_label = QLabel(f"{p['name']} - Price:{p['price']} - Qty:{p['quantity']}")
                     self.owned_products_layout.addWidget(p_label)

             # Clear transactions layout
             for i in reversed(range(self.transactions_layout.count())):
                 w = self.transactions_layout.itemAt(i).widget()
                 if w:
                     w.setParent(None)

             transactions = response.get("transactions", [])
             if not transactions:
                 no_txn = QLabel("No transactions")
                 no_txn.setAlignment(Qt.AlignCenter)
                 self.transactions_layout.addWidget(no_txn)
             else:
                 for t in transactions:
                     t_label = QLabel(f"Buyer:{t['buyer_id']} Seller:{t['seller_id']} Product:{t['product_name']} "
                                      f"Qty:{t['quantity']} Price:{t['sale_price']} Date:{t['date']}")
                     self.transactions_layout.addWidget(t_label)
         else:
             QMessageBox.warning(self, "Error", response.get("message", "Could not load portfolio"))


class Ui_LoginPage(object):


    def setupUi(self, Widget):
        Widget.setObjectName("LoginPage")
        Widget.setStyleSheet("background-color: #2E8B57;")  # Soft Teal Color

        self.main_layout = QVBoxLayout(Widget)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.main_layout.setSpacing(30)

        # Title Label
        self.label_title = QLabel("Login", Widget)
        font = QFont()
        font.setFamily("Snap ITC")
        font.setPointSize(36)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: white;")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label_title)

        # Form Layout
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(20)
        self.form_layout.setAlignment(Qt.AlignHCenter)

        self.lineEdit_username = QLineEdit(Widget)
        self.lineEdit_username.setPlaceholderText("User Name")
        self.lineEdit_username.setFixedWidth(300)
        self.lineEdit_username.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                border: none;
                border-bottom: 2px solid #FFFFFF;
                color: #000000;
                padding-bottom: 7px;
                font-size: 18px;
            }
            QLineEdit::placeholderText {
                color: gray;
            }
        """)
        self.form_layout.addWidget(self.lineEdit_username)

        self.lineEdit_password = QLineEdit(Widget)
        self.lineEdit_password.setPlaceholderText("Password")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setFixedWidth(300)
        self.lineEdit_password.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                border: none;
                border-bottom: 2px solid #FFFFFF;
                color: #000000;
                padding-bottom: 7px;
                font-size: 18px;
            }
            QLineEdit::placeholderText {
                color: gray;
            }
        """)
        self.form_layout.addWidget(self.lineEdit_password)

        self.main_layout.addLayout(self.form_layout)

        # Login Button
        self.pushButton_login = QPushButton("Log In", Widget)
        self.pushButton_login.setFixedHeight(50)
        self.pushButton_login.setFixedWidth(200)
        self.pushButton_login.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border-radius: 5px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #63B8FF;
            }
        """)
        self.main_layout.addWidget(self.pushButton_login, 0, Qt.AlignHCenter)

        self.label_switch = QLabel("Don't have an account?", Widget)
        self.label_switch.setStyleSheet("color: white; font-size:16px;")
        self.label_switch.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label_switch)

        self.pushButton_register = QPushButton("Register here", Widget)
        self.pushButton_register.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                text-decoration: underline;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #FFD700;
            }
        """)
        self.pushButton_register.setCursor(Qt.PointingHandCursor)
        self.main_layout.addWidget(self.pushButton_register, 0, Qt.AlignHCenter)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("LoginPage", "Login"))

class Ui_RegisterPage(object):


    def setupUi(self, Widget):
        Widget.setObjectName("RegisterPage")
        Widget.setStyleSheet("background-color: #2E8B57;")  # Soft Teal Color

        self.main_layout = QVBoxLayout(Widget)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.main_layout.setSpacing(30)

        self.label_title = QLabel("Register", Widget)
        font = QFont()
        font.setFamily("Snap ITC")
        font.setPointSize(36)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: white;")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label_title)

        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(20)
        self.form_layout.setAlignment(Qt.AlignHCenter)

        self.lineEdit_username = QLineEdit(Widget)
        self.lineEdit_username.setPlaceholderText("Username")
        self.lineEdit_username.setFixedWidth(300)
        self.lineEdit_username.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                border: none;
                border-bottom: 2px solid #1E90FF;
                color: #000000;
                padding-bottom: 7px;
                font-size: 18px;
            }
            QLineEdit::placeholderText {
                color: gray;
            }
        """)
        self.form_layout.addWidget(self.lineEdit_username)

        self.lineEdit_email = QLineEdit(Widget)
        self.lineEdit_email.setPlaceholderText("Email")
        self.lineEdit_email.setFixedWidth(300)
        self.lineEdit_email.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                border: none;
                border-bottom: 2px solid #1E90FF;
                color: #000000;
                padding-bottom: 7px;
                font-size: 18px;
            }
        """)
        self.form_layout.addWidget(self.lineEdit_email)

        self.lineEdit_name = QLineEdit(Widget)
        self.lineEdit_name.setPlaceholderText("Name")
        self.lineEdit_name.setFixedWidth(300)
        self.lineEdit_name.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                border: none;
                border-bottom: 2px solid #1E90FF;
                color: #000000;
                padding-bottom: 7px;
                font-size: 18px;
            }
        """)
        self.form_layout.addWidget(self.lineEdit_name)

        self.lineEdit_password = QLineEdit(Widget)
        self.lineEdit_password.setPlaceholderText("Password")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setFixedWidth(300)
        self.lineEdit_password.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                border: none;
                border-bottom: 2px solid #1E90FF;
                color: #000000;
                padding-bottom: 7px;
                font-size: 18px;
            }
        """)
        self.form_layout.addWidget(self.lineEdit_password)

        self.main_layout.addLayout(self.form_layout)

        self.pushButton_register = QPushButton("Register", Widget)
        self.pushButton_register.setFixedHeight(50)
        self.pushButton_register.setFixedWidth(200)
        self.pushButton_register.setStyleSheet("""
            QPushButton {
                background-color: #1F95EF;
                color: white;
                border-radius: 5px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #166BB5;
            }
        """)
        self.main_layout.addWidget(self.pushButton_register, 0, Qt.AlignHCenter)

        self.label_switch = QLabel("Already have an account?", Widget)
        self.label_switch.setStyleSheet("color: white; font-size:16px;")
        self.label_switch.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label_switch)

        self.pushButton_login = QPushButton("Login here", Widget)
        self.pushButton_login.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                text-decoration: underline;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #FFD700;
            }
        """)
        self.pushButton_login.setCursor(Qt.PointingHandCursor)
        self.main_layout.addWidget(self.pushButton_login, 0, Qt.AlignHCenter)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("RegisterPage", "Register"))


class WelcomePage(QWidget, Ui_WelcomePage):
     switch_to_login = pyqtSignal()
     switch_to_register = pyqtSignal()

     def __init__(self):
         super(WelcomePage, self).__init__()
         self.setupUi(self)
         #Connect signals instead of using emit
         self.pushButton.clicked.connect(self.switch_to_login)
         self.pushButton_2.clicked.connect(self.switch_to_register)

class LoginPage(QWidget, Ui_LoginPage):
     switch_to_register = pyqtSignal()
     login_successful = pyqtSignal(str,int)  # Emits username on successful login

     def __init__(self):
         super(LoginPage, self).__init__()
         self.setupUi(self)
         self.pushButton_login.clicked.connect(self.handle_login)
         self.pushButton_register.clicked.connect(self.switch_to_register)

     def handle_login(self):
         """
         Handles the login process by sending credentials to the server.
         """
         username = self.lineEdit_username.text().strip()
         password = self.lineEdit_password.text().strip()
         usernameA_[0] = username
         if not username or not password:
             QMessageBox.warning(self, "Input Error", "Please fill in both username and password.")
             return

         # Prepare login data
         login_data = {
             "action": "LOGIN",
             "username": username,
             "password": password
         }

         # Send data to the server
         response = send_data(login_data)

         if response.get("status") == "success":
             QMessageBox.information(self, "Login Successful", response.get("message"))
             logged_in_username = response.get("username", username)
             logged_in_user_id = response.get("user_id",None)
             self.clear_fields()
             self.login_successful.emit(logged_in_username,logged_in_user_id)
         else:
             QMessageBox.warning(self, "Login Failed", response.get("message"))
             # Optionally, emit a signal to switch to Register page
             # self.switch_to_register.emit()



     def clear_fields(self):
         """
         Clears all input fields after successful login.
         """
         self.lineEdit_username.clear()
         self.lineEdit_password.clear()

class RegisterPage(QWidget, Ui_RegisterPage):
     switch_to_login = pyqtSignal()

     def __init__(self):
         super(RegisterPage, self).__init__()
         self.setupUi(self)
         self.pushButton_register.clicked.connect(self.handle_register)
         self.pushButton_login.clicked.connect(self.switch_to_login)
     def handle_register(self):
         """
         Handles the registration process by sending user details to the server.
         """
         username = self.lineEdit_username.text().strip()
         email = self.lineEdit_email.text().strip()
         name = self.lineEdit_name.text().strip()
         password = self.lineEdit_password.text().strip()

         if not username or not email or not name or not password:
             QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
             return

         # Prepare registration data
         register_data = {
             "action": "REGISTER",
             "username": username,
             "password": password,
             "email": email,
             "name": name
         }

         # Send data to the server
         response = send_data(register_data)

         if response.get("status") == "success":
             QMessageBox.information(self, "Registration Successful", response.get("message"))
             self.clear_fields()
             self.switch_to_login.emit()  # Redirect to Login after successful registration
         else:
             QMessageBox.warning(self, "Registration Failed", response.get("message"))



     def clear_fields(self):
         """
         Clears all input fields after successful registration.
         """
         self.lineEdit_username.clear()
         self.lineEdit_email.clear()
         self.lineEdit_name.clear()
         self.lineEdit_password.clear()

class MainMenuPage(QWidget, Ui_MainMenuPage):
     logout_signal = pyqtSignal()

     def __init__(self, parent = None):
         super(MainMenuPage, self).__init__(parent)
         self.setupUi(self)  # Set up the UI defined in Ui_MainMenuPage
         self.username = None
         self.current_user_id = None
         self.pushButton_9.clicked.connect(self.logout_signal.emit)
         self.pushButton_15.clicked.connect(self.logout_signal.emit)



class MainApplication(QMainWindow):
    def __init__(self):
        super(MainApplication, self).__init__()

        # Initialize QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize Pages
        self.welcome_page = WelcomePage()
        self.login_page = LoginPage()
        self.register_page = RegisterPage()

        # Add Pages to StackedWidget
        self.stacked_widget.addWidget(self.welcome_page)  # Index 0
        self.stacked_widget.addWidget(self.login_page)  # Index 1
        self.stacked_widget.addWidget(self.register_page)  # Index 2

        # Connect Signals for Navigation
        self.welcome_page.switch_to_login.connect(self.show_login)
        self.welcome_page.switch_to_register.connect(self.show_register)

        self.login_page.switch_to_register.connect(self.show_register)
        self.login_page.login_successful.connect(self.show_main_menu)

        self.register_page.switch_to_login.connect(self.show_login)

        # Set initial page to Welcome
        self.stacked_widget.setCurrentIndex(0)

    def show_login(self):
        """
        Switch to the Login page.
        """
        self.stacked_widget.setCurrentIndex(1)

    def show_register(self):
        """
        Switch to the Register page.
        """
        self.stacked_widget.setCurrentIndex(2)

    def show_main_menu(self, username, user_id):
        """
        Switch to the Main Menu page after a successful login.
        """
        print("before adding main_menu_page")
        if not hasattr(self, "main_menu_page") or self.main_menu_page is None:
            # Dynamically create the MainMenuPage when needed
            print("Creating main_menu_page ")
            self.main_menu_page = MainMenuPage()
            self.stacked_widget.addWidget(self.main_menu_page)
            print("MainMenuPage added to stacked widget")
            self.main_menu_page.logout_signal.connect(self.show_welcome)
            print("Logout signal detected")
        print("switching to main_menu_page")
        # Switch to Main Menu
        self.main_menu_page.username = username
        self.main_menu_page.current_user_id = user_id
        self.stacked_widget.setCurrentWidget(self.main_menu_page)
        print("Main menu shown")
        QMessageBox.information(self, "Welcome", f"Welcome, {username}!")

    def show_welcome(self):
        """
        Switch back to the Welcome page (e.g., after logout).
        """
        self.stacked_widget.setCurrentIndex(0)



def main():
    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()