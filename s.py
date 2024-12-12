import socket
import threading
import json
import time


def Communicate_Server(clientA, clientB, usernameA, usernameB, server_socket):

  def send_data(client, data):
    json_data = json.dumps(data)
    client.send(json_data.encode('utf-8'))

  def listen_for_requests(alive,client,requests):
    while alive[0]:
      json_data = client.recv(1024).decode('utf-8')
      request = json.loads(json_data)
      requests.append(request)
      #print(f"{request} appended")
      time.sleep(2)
    print("Not listening anymore")
    return

  def process_requests(alive, clients, requests, conversation, server_socket):
    messages_going_to_A = []
    messages_going_to_B = []
    clientA = clients[0]
    clientB = clients[1]
    while alive[0]:
      if len(requests) != 0:
        currently_processing = requests.pop(0)
        print(currently_processing)        
        if currently_processing["action"] == "SEND_MESSAGE":
          #print("Preparing to add to queue")
          if currently_processing["sender"] == usernameA:
            #print("Appending to queue B")
            messages_going_to_B.append(currently_processing)
          elif currently_processing["sender"] == usernameB:
            #print("Appending to queue A")
            messages_going_to_A.append(currently_processing)
          conversation.append(currently_processing)
            
        
        elif currently_processing["action"] == "RECEIVE_MESSAGE":
          #print("Preparing to send queue")
          RECEIVE_MESSAGE_RESPONSE = {
            "action":"RECEIVE_MESSAGE_RESPONSE",
            "content":[]
          }
          if currently_processing["sender"] == usernameA:
            RECEIVE_MESSAGE_RESPONSE["content"] = messages_going_to_A.copy()
            send_data(clientA,RECEIVE_MESSAGE_RESPONSE)
            messages_going_to_A = []
          elif currently_processing["sender"] == usernameB:
            RECEIVE_MESSAGE_RESPONSE["content"] = messages_going_to_B.copy()
            send_data(clientB,RECEIVE_MESSAGE_RESPONSE)
            messages_going_to_B = []
          else:
            continue
        
        elif currently_processing["action"] == "TERMINATE":
          TERMINATE_RESPONSE = {
            "action":"TERMINATE_RESPONSE"
          }
          if currently_processing["sender"] == usernameA:
            send_data(clientB,TERMINATE_RESPONSE)
          
          elif currently_processing["sender"] == usernameB:
            send_data(clientA,TERMINATE_RESPONSE)

          alive[0] = False
          for i in range(3, 0, -1):
            print(f"Closing the server side in {i}...")
            time.sleep(1)

          return        

  def communicate(clientA, clientB, server_socket):
      
      alive = [True]
      requests = []
      conversation = []
      clients = [clientA, clientB]
      
      try:
        t1 = threading.Thread(target=listen_for_requests, args=(alive, clients[0], requests)).start()
        t2 = threading.Thread(target=listen_for_requests, args=(alive, clients[1], requests)).start()
        t3 = threading.Thread(target=process_requests, args=(alive, clients, requests, conversation, server_socket)).start()
      except:
        print("Closing server")
        return
      print("About to close server side socket")
      server_socket.close()
      print("Server side closed")  

  return communicate(clientA, clientB, server_socket)


def get_username_from_socket(username, socket_username_list):
  for socket_username in socket_username_list:
    if socket_username[1] == username:
      return socket_username[0]
  return


def Initiate_Server():
    
    def send_data(client, data):
      #print(f"Sending {data} to {client}")
      json_data = json.dumps(data)
      client.send(json_data.encode('utf-8'))
      #print("Sent")
      return json.loads(client.recv(1024).decode('utf-8'))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8078))
    socket_username_list = []
    #print("Server started on localhost:8000. Waiting for connections...")
    
    def Initiate_Communicate(server_socket, client_socket, socket_username_list, sender, receiver):
     
      socket_username_list.append([client_socket,sender])
      
      clientA = client_socket
      usernameA = sender
      
      usernameB = receiver
      clientB = None
      #print(socket_username_list)
      while clientB == None:
        clientB = get_username_from_socket(receiver, socket_username_list)
        time.sleep(2)
      
      Communicate_Server(clientA, clientB, usernameA, usernameB, server_socket)
    
    socket_username_list = []
    for i in range(10): # While True in the future
      try:

        server_socket.listen()
        client_socket, address = server_socket.accept()
        
        GET_USERNAMES = {
          "action": "GET_USERNAMES",
        }

        response = send_data(client_socket,GET_USERNAMES)
        sender = response["content"][0]
        receiver = response["content"][1]
        clientThread = threading.Thread(target=Initiate_Communicate,args=(server_socket, client_socket, socket_username_list, sender, receiver))
        clientThread.start()
      except:
        server_socket.close()
        return
      
#Initiate_Server()