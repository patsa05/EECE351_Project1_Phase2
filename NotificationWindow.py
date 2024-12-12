from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QLineEdit, QGridLayout, QMainWindow, QComboBox

from client import run_communicate, getUsernameA
from client_helper import askClientList, askAllClientList

from array_ui import Ui_MainWindow

from multiprocessing import Process

import json

import os

from socket import *


def contact(usernameA, usernameB, client_socket):
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(('localhost',8080))
        def initiate_communication():
            INITIATE_COMMUNICATION = {
            "action":"INITIATE_COMMUNICATION",
            "sender":usernameA,
            "receiver":usernameB
            }
            json_data = json.dumps(INITIATE_COMMUNICATION)
            client_socket.sendall(json_data.encode('utf-8')) # Allow the server to notify {usernameB} that {usernameA} wants to chat

        def ip_port_of_peer_request():
            IP_PORT_OF_PEER_REQUEST = {
                "action":"IP_PORT_OF_PEER_REQUEST",
                "key":(usernameA,usernameB)
            }
            json_data = json.dumps(IP_PORT_OF_PEER_REQUEST)
            client_socket.sendall(json_data.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            response = json.loads(response)
            return response["content"]
        
        def update_ip_port_on_server_request(IP,PORT):
            UPDATE_IP_PORT_ON_SERVER_REQUEST = {
                "action":"UPDATE_IP_PORT_ON_SERVER_REQUEST",
                "key":(usernameA,usernameB), # i.e. (receiver,sender) <=> (user that hosts the server, user that connects to server side)
                "value": (IP,PORT) 
            }
            json_data = json.dumps(UPDATE_IP_PORT_ON_SERVER_REQUEST)
            client_socket.sendall(json_data.encode('utf-8')) 

        try: # Try to connect to the peer
            client_socket_p2p = socket(AF_INET, SOCK_STREAM) 
            (IP,PORT) = ip_port_of_peer_request()
            client_socket_p2p.connect((IP,PORT))
            client_socket_p2p.close()

        except Exception as e: # If it isn't possible (i.e. peer not connected to chat app) then open server side to allow peer to join
            (IP,PORT) = ('localhost',8078)
            update_ip_port_on_server_request(IP,PORT)
            #client_socket_p2p = socket(AF_INET, SOCK_STREAM)
            ip_port = IP+":"+str(PORT)
            true_flag = "True"
            command = f"python init_chat.py {usernameA} {usernameB} {ip_port} {true_flag} client_socket_p2p_id"            
            
        
        initiate_communication()
        client_socket.close()
        ip_port = IP+":"+str(PORT)
        true_flag = "False"
        command = f"python init_chat.py {usernameA} {usernameB} {ip_port} {true_flag} client_socket_p2p_id"
        os.system(command)

    except Exception as e:
        print("problem in contact", e)
        client_socket_p2p.close()
        return
    
    

# Main window class
class NotificationWindow(QWidget):
    def __init__(self,usernameA_,client_socket):
        super().__init__()
        self.setWindowTitle("Notification")
        self.resize(400, 400)
        self.usernameA_ = usernameA_
        self.client_socket = client_socket
        # Store notifications (initially empty)
        self.notifications = []

        # Main layout
        self.main_layout = QVBoxLayout(self)

        # Input layout for dropdown contact
        self.input_layout = QHBoxLayout()
        self.user_dropdown = QComboBox()  # Create a QComboBox for dropdown
        self.user_dropdown.setPlaceholderText("Select username...")  # Set placeholder text

        self.contact_button = QPushButton("Contact")
        self.contact_button.clicked.connect(lambda: self.contact_from_input()) 
        self.input_layout.addWidget(self.user_dropdown)  # Add dropdown to layout
        self.input_layout.addWidget(self.contact_button)
        self.main_layout.addLayout(self.input_layout)


        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.update_notifications)
        self.main_layout.addWidget(self.refresh_button)

        # Scroll area for notifications
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

    def contact_from_input(self):
        """
        Handles contacting a user typed in the input field.
        """
        user = self.user_dropdown.currentText()
        if user:
            #contact(user)
            #usernameA = input("Sender: ")
            usernameB = user
            process = Process(target=contact, args=(self.usernameA_[0],usernameB,self.client_socket,))
            process.start()
            #process.join() 
        else:
            print("Please enter a valid username.")

    def update_notifications(self):
        """
        Updates the notification list with new entries.
        """
        
        clients = askAllClientList(self.usernameA_[0],self.client_socket)
        self.user_dropdown.clear()
        for client in clients:
            if client.strip():
                self.user_dropdown.addItem(client)

        self.notifications = askClientList(self.usernameA_[0],self.client_socket)
        # Clear existing layout
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add new notifications
        for user in self.notifications:
            if not (user.__contains__(" ") or user.__contains__(",")):
                self.add_notification(user)

    def contact_from_list(self,user):
        usernameB = user
        process = Process(target=contact, args=(self.usernameA_[0],usernameB,self.client_socket,))
        process.start()
        process.join()

    def add_notification(self, user):
        """
        Adds a single notification entry to the UI.
        """
        notification_layout = QHBoxLayout()
        label = QLabel(user)
        contact_button = QPushButton("Contact")
        #usernameA = input("Sender: ")
        usernameB = user
        contact_button.clicked.connect(lambda: self.contact_from_list(user))  # Link the button to the contact function
        notification_layout.addWidget(label)
        notification_layout.addWidget(contact_button)
        self.scroll_layout.addLayout(notification_layout)
