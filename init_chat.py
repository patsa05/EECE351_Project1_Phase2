import argparse
import socket
import sys
import json
import time
import threading

from client import run_communicate

from socket import *


def parse_arguments():
    parser = argparse.ArgumentParser(description="Setup communication with peer-to-peer connection.")
    
    # Arguments for usernameA and usernameB (strings)
    parser.add_argument("usernameA", type=str, help="Username of the first user")
    parser.add_argument("usernameB", type=str, help="Username of the second user")
    
    # Argument for IP and PORT (combined in a single string, e.g., '127.0.0.1:8080')
    parser.add_argument("ip_port", type=str, help="IP and PORT of the peer in the format IP:PORT")
    
    # Argument for True (boolean flag)
    parser.add_argument("true", type=bool, help="True flag for connection establishment")
    
    # Argument for client_socket_p2p (example: socket identifier or placeholder)
    parser.add_argument("client_socket_p2p", type=str, help="Client socket identifier or placeholder")
    
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()
    print("Here")
    # Extract arguments
    usernameA = args.usernameA
    usernameB = args.usernameB
    
    # Parse the IP and PORT from the ip_port argument
    ip, port = args.ip_port.split(':')
    port = int(port)
    client_socket_p2p = socket(AF_INET, SOCK_STREAM)
    # Assuming the run_communicate function is available and imported
    # You can now call the run_communicate function with the parsed arguments
    
    run_communicate(usernameA, usernameB, (ip, port), args.true, client_socket_p2p)

if __name__ == "__main__":
    print("Hi")
    main()
