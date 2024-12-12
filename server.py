import sys
from socket import socket, AF_INET, SOCK_STREAM
from database import create_tables
from config import DEFAULT_IP, DEFAULT_PORT, BUFFER_SIZE
import threading
from server_helper import handle_client

# --- Server Script Overview ---

# 1. Imports and Configuration
# - `sys`: Used to handle command-line arguments.
# - `socket` from `socket`: Provides networking capabilities.
# - `create_tables` from `database`: Initializes database schema.
# - `DEFAULT_IP`, `DEFAULT_PORT`, `BUFFER_SIZE` from `config`: Default server settings.
# - `threading`: Enables handling multiple clients simultaneously.
# - `handle_client` from `server_helper`: Processes client requests.

# 2. Create Server Socket
# Function: `create_server_socket(ip, port)`
# - Binds the server to the provided IP and port.
# - Configures the socket to listen for incoming connections.
# - Returns the server socket object.

# 3. Main Function
# Function: `main()`
# - Parses command-line arguments for server IP and port.
# - If arguments are not provided, defaults to `DEFAULT_IP` and `DEFAULT_PORT`.
# - Calls `create_server_socket` to set up the server.
# - Initializes the database tables using `create_tables`.
# - Creates `socket_username_array` and `message_queue` to manage client sockets and messages.

# 4. Accept Connections
# - Enters a loop to accept client connections.
# - Adds each new connection to `socket_username_array` and `message_queue`.
# - Creates a new thread for each client using `handle_client`.

# 5. Handle Shutdown
# - Handles a `KeyboardInterrupt` to allow graceful shutdown.
# - Ensures the server socket is closed properly on exit.

# 6. Entry Point
# - Executes `main()` when the script is run directly.




























def create_server_socket(ip, port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()
    return server_socket

def main():
    if len(sys.argv) < 3:
        print('Usage: "python server.py server_ip port_number"')
        ip = DEFAULT_IP
        port = DEFAULT_PORT
    else:
        ip = sys.argv[1]
        port = int(sys.argv[2])

    server_socket = create_server_socket(ip, port)
    print(f"Server is listening on {ip}:{port}")
    
    create_tables()
    socket_username_array = []
    message_queue = []
    usernames_to_ip_port = []
    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"New connection from {address}")
            socket_username_array.append([client_socket, ""])
            message_queue.append([client_socket, ""])
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, address, socket_username_array,message_queue,usernames_to_ip_port)
            )
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()