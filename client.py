import socket
import time
import threading
import sys
import select
from random import random
import msvcrt


STATE_LOOKING_FOR_SERVER = 0
STATE_CONNECTING_TO_SERVER = 1
STATE_GAME_MODE = 2
class Client:
    def __init__(self):
        print("Client started, listening for offer requests")
        self.name = 'Chovav'+'\n' #TODO: randomly pick names
        # Define server address and port for UDP
        self.udp_listen_address = ('0.0.0.0', 13117)
        self.tcp_server_address = None
        # Define client states
        self.state = STATE_LOOKING_FOR_SERVER
        # Define TCP socket
        self.MAGIC_COOKIE = 0xabcddcba.to_bytes(4, byteorder='big')
        self.tcp_client_socket = None
        self.waiting_for_input = False


    # Function to handle state: Looking for a server
    def state_looking_for_server(self):
        udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_client_socket.bind(self.udp_listen_address)
        udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while True: #TODO: consider changing the condition or adding sleep
            data, server_address = udp_client_socket.recvfrom(1024)
            magic_cookie = data[:4]
            message_type = data[4]
            if magic_cookie == self.MAGIC_COOKIE and message_type == 2:
                server_name = data[5:37].decode('utf-8').strip()
                tcp_port = int.from_bytes(data[37:], byteorder='big')
                print("Received offer from server:", server_name)
                print("Server IP address:", server_address[0])
                print("TCP port:", tcp_port)
                print("Attempting to connect...")
                self.tcp_server_address = (server_address[0], tcp_port)
                udp_client_socket.close()
                self.tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                return STATE_CONNECTING_TO_SERVER
            time.sleep(1)


    # Function to handle state: Connecting to a server
    def state_connecting_to_server(self):
        try:
            self.tcp_client_socket.connect(self.tcp_server_address)
            self.tcp_client_socket.sendall(self.name.encode('utf-8'))
            print("Connected to TCP server.")
            return STATE_GAME_MODE
        except Exception as e:
            print("Failed to connect to server:", e)
            return STATE_LOOKING_FOR_SERVER

    def get_messages_from_server(self):
        while True:
            try:
                message = self.tcp_client_socket.recv(1024).decode('utf-8')
                if not message:
                    print("Server disconnected, listening for offer requests...")
                    self.tcp_client_socket.close()
                    self.state = STATE_LOOKING_FOR_SERVER
                    break
                else:
                    print(message)
            except Exception as e:
                print("Error while getting message from the server:", e)
                # Close the TCP socket
                #self.tcp_client_socket.close()

    def get_user_input(self):
        while True: #TODO: consider changing the condition
            if self.state == STATE_GAME_MODE:
                try:
                    user_input = input()
                    self.tcp_client_socket.sendall(user_input.encode('utf-8'))
                except Exception as e:
                    print("Error while getting keyboard input:", e)
            else:
                time.sleep(1)

    # Function to handle state: Game mode
    def game_mode(self):
        print("Entering game mode...")
        listen_thread = threading.Thread(target=self.get_messages_from_server)
        listen_thread.start()
        listen_thread.join()

    # Main function to run the client
    def run_client(self):
        keyboard_thread = threading.Thread(target=self.get_user_input)
        keyboard_thread.start()
        while True:  # TODO: CHANGE IT TO DIFFERENT CONDITION
            if self.state == STATE_LOOKING_FOR_SERVER:
                self.state = self.state_looking_for_server()
            elif self.state == STATE_CONNECTING_TO_SERVER:
                self.state = self.state_connecting_to_server()
            elif self.state == STATE_GAME_MODE:
                self.game_mode()



# Create an instance of the GameClient class and run the client
if __name__ == "__main__":
    client = Client()
    client.run_client()