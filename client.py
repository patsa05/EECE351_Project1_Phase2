import sys
from client_helper import *
from config import DEFAULT_IP, DEFAULT_PORT
from socket import socket, AF_INET, SOCK_STREAM

from s import Initiate_Server
from array_ui import Ui_MainWindow 
from PyQt5 import QtCore, QtGui, QtWidgets 


############################################################################

#client_socket = connect_to_server()

global usernameA 
usernameA = None

def getUsernameA():
    if usernameA:
        return usernameA


############################################################################################################################################
#COMMUNICATE_CLIENT(): facilitates client-client communication over a socket and manages message sending, recieving and conversation flows
#send_data(client_socket, data):
#Sends serialized JSON data over the provided socket.
#printing(sender, receiver, conversation, alive, in_typing_mode):
#Continuously updates the console with the conversation unless typing mode is enabled.
#receive_new_messages(alive, in_typing_mode, conversation, client_socket):
#Continuously listens for new messages from the server and updates the conversation list. Terminates on server disconnect.
#send_a_message(alive, in_typing_mode, message, client_socket):
#Sends a new message to the server for delivery to the recipient.
#take_input(alive, in_typing_mode, conversation, client_socket, action):
#Handles user input for typing or ending communication. Updates the conversation locally and sends data to the server.
######################################################################################################################################################



################################################################################################################################################################

def Communicate_Client(usernameA, usernameB, client_socket, window):

  def send_data(client_socket, data):
      """Send JSON data to the server."""
      json_data = json.dumps(data)
      client_socket.sendall(json_data.encode('utf-8'))
      
  def receive_new_messages(alive, in_typing_mode, conversation, client_socket):
      """Listen for new messages from the server."""
      while alive[0]:
        try:
            request = {
                "action": "RECEIVE_MESSAGE",
                "sender": usernameA 
              }
            send_data(client_socket, request)
            response = client_socket.recv(1024).decode('utf-8')
            if response:
                if json.loads(response)["action"] == "TERMINATE_RESPONSE":
                  alive[0] = False
                  print("Communication terminated")
                  return
                new_messages = json.loads(response).get("content", [])
                for message in new_messages:
                  #print(conversation)
                  conversation.append(message["content"])
                  window[0].add_to_chat_display(message["content"]) ##############################################################
                  
            time.sleep(5)
        except:
            print("Communication terminated")
            return

  def send_a_message(message, client_socket):
      """Send a message to the server."""
      SEND_MESSAGE = {
          "action": "SEND_MESSAGE",
          "sender": usernameA,
          "receiver": usernameB,
          "content": str(usernameA) + ": " + str(message)
      }
      send_data(client_socket, SEND_MESSAGE)
      print(SEND_MESSAGE)

  def take_input(conversation, client_socket):
    """Handle user input for messaging."""
    to_send = window[0].get_message() #input("Input your message: ")
    send_a_message(to_send, client_socket) # Send to peer
    conversation.append(f"{usernameA}: {to_send}") # Store in the conversation array
    window[0].add_to_chat_display(f"{usernameA}: {to_send}") # Display it on the window
  
  alive = [True]
  conversation = []
  action = [""]
  in_typing_mode = [False]

  #ask_for_previous_conversation(conversation,usernameA)

  request = json.loads(client_socket.recv(1024).decode('utf-8'))

  if request["action"] == "GET_USERNAMES":
    send_data(client_socket, {"action":"GET_USERNAMES_RESPONSE", "content":(usernameA,usernameB)})

  window[1].show()
  
  window[0].sendButton.clicked.connect(lambda: take_input(conversation, client_socket))

  threading.Thread(target=receive_new_messages, args=(alive, in_typing_mode, conversation, client_socket)).start()

######################################################################################################################################################

def run_communicate(usernameA,usernameB,IPPORT,exception,client_socket_p2p):
    
    def terminate(client_socket, usernameA):           
        TERMINATE = {
        "action":"TERMINATE",
        "sender":usernameA
        }
        json_data = json.dumps(TERMINATE)
        client_socket.sendall(json_data.encode('utf-8'))
        return

    (IP,PORT) = IPPORT

    if exception:
        print("HI")
        t1 = threading.Thread(target=Initiate_Server, args=()).start()
        client_socket_p2p.connect((IP,PORT))
    
    # Setting up the window
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    window=[ui,MainWindow]
    Communicate_Client(usernameA,usernameB,client_socket_p2p,window)
    try:
        app.exec_()
        terminate(client_socket_p2p,usernameA)
    except Excpetion as e:
        print("Failed to terminate server side of peer")
        print(f"Exception: {e}")

######################################################################################################################################################

def connect_to_server():
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 8080))
        print("Connected to server successfully!")
        return client_socket
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return None

######################################################################################################################################################



#######################################################################################################################################
# Main Function Logic:
# Handles user authentication, displays menus, and redirects to appropriate functionality
# CONNECT_TO_SERVER() : socket connection to server, returns socket object
# RUN_COMMUNICATE() : Initiates the communication feature by connecting to a local socket and launching COMMUNICATE_CLIENT()
##################################################################################################################################################



####################################################################################################################################################
#MarketPlace Features:
#welcome_page():
#Displays the application's welcome screen.
#login(username_alias):
#Handles user login and updates username_alias with the logged-in user's name.
#register():
#Facilitates new user registration.
#main_menu():
#Displays the primary menu options.
###########################################################################################################################################################





##########################################################################################################################################################
#Product Mangement
#view_products():
#Fetches and displays available products in the marketplace. Returns details for further processing.
#view_owner(owner_chosen, product_id):
#Displays the details of a selected owner and product.
#add_product(username):
#Allows the logged-in user to add a new product to the marketplace.
#buy_product(user_id, product_id, quantity):
#Handles the purchase of a product by a user.
##################################################################################################################################################################




############################################################################################################################################################################
# User Management
#view_portfolio(username):
#Displays the logged-in user's portfolio.
#add_funds(user_id):
#Lets a user add funds to their account.
#askClientList():
#Retrieves a list of other connected users.
#want_communication(usernameA, usernameB):
#Confirms if a user wants to initiate communication with another.
#######################################################################################################################################################################################




########################################################################################################################################

def main():
   # client_socket = connect_to_server()
    if not client_socket:
        print("Could not connect to server. Please make sure the server is running.")
        return
    username_alias = [""]
    try:
        while True:
            welcome_page() 
            choice = input("\nSelect an option: ")
            if not choice.isdigit():
                print("\nPlease enter a number: ")
                continue
                
            choice = int(choice)
            if choice == 1:
                if login(username_alias):
                    while True:
                        main_menu()
                        main_choice = int(input("\nEnter your choice: "))
                        if main_choice == 1:
                            print("\nProducts in the market: ")
                            owner, product_name = view_products()
                        elif main_choice == 2:
                                print("\nProducts in the market: ")
                                owner, product_name = view_products()
                                owner_chosen = input("\nSelect owner: ")
                                product_id = input("\nEnter the product ID: ")
                                view_owner(owner_chosen, product_id)
                                if want_communication(username_alias[0], owner_chosen):
                                    run_communicate()
                        elif main_choice == 3:
                            print("\nAdding product....")
                            add_product(username_alias[0])
                        elif main_choice == 4:
                            print("Buying product....")
                            user_id = input("\nEnter your user_id: ")
                            product_id = input("\nEnter the product's id: ")
                            quantity = int(input("\nEnter quantity to purchase: "))
                            buy_product(user_id, product_id, quantity)

                        elif main_choice == 5:
                            username = input("\nEnter your username: ")
                            print("Viewing Portfolio...")
                            view_portfolio(username)

                        elif main_choice == 6:
                            user_id = input("\nEnter your user ID: ")
                            add_funds(user_id)
                        
                        elif main_choice == 7: 
                            pending_notifications_username_list = askClientList()
                            print("Notifications from: ")
                            print(pending_notifications_username_list)
                            owner_chosen = input("Who do you want to contact ?: ")
                            if want_communication(username_alias[0],owner_chosen ):
                                run_communicate()
                                continue 
                        elif main_choice == 8:
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice, please try again.")

            elif choice == 2:
                register()
            elif choice == 3:
                print("Thank you for visiting AUBoutique!")
                break
            else:
                print("Invalid Option!")


    except Exception as f:
        print(f"an error occurred {f}")
'''
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        client = connect_to_server(ip, port)
    main()
'''
###########################################################################################################################################################################################################################################################################

