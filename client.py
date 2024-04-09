# import socket
#
# # Define server address and port
# SERVER_ADDRESS = ('localhost', 8888)
#
# # Create a UDP socket
# udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # Send data to the server
# message = "Hello, server!"
# message = "my name is Amit"
# udp_client_socket.sendto(message.encode('utf-8'), SERVER_ADDRESS)
#
# # Receive response from the server
# response, server_address = udp_client_socket.recvfrom(1024)
# print(f"Received response from server: {response.decode('utf-8')}")
# new_message = input("my answer is:")
# udp_client_socket.sendto(new_message.encode('utf-8'), SERVER_ADDRESS)
#
# # Close the connection
# udp_client_socket.close()
# #
# # import socket
# #
# # # Define server address and port
# # SERVER_ADDRESS = ('localhost', 8888)
# #
# # # Create a UDP socket
# # udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #
# # # Main loop
# # while True:
# #     try:
# #         # Receive question from the server
# #         data, server_address = udp_client_socket.recvfrom(1024)
# #         question = data.decode('utf-8')
# #
# #         # Print the question and get user's answer
# #         print(f"Question: {question}")
# #         answer = input("Your answer: ")
# #
# #         # Send answer to the server
# #         udp_client_socket.sendto(answer.encode('utf-8'), SERVER_ADDRESS)
# #
# #         # Receive feedback from the server
# #         data, server_address = udp_client_socket.recvfrom(1024)
# #         feedback = data.decode('utf-8')
# #
# #         # Print feedback
# #         print(feedback)
# #
# #     except Exception as e:
# #         print(f"Error: {e}")
# #         break
# #
# # # Close the socket
# # udp_client_socket.close()


# import socket
#
# # Define server address and port for UDP
# UDP_SERVER_ADDRESS = ('<broadcast>', 8889)
#
# # Define server address and port for TCP
# TCP_SERVER_ADDRESS = ('localhost', 8889)
#
# # Define the UDP broadcast message
# BROADCAST_MESSAGE = "Hello, this is the server!"
#
# # Create a UDP socket for receiving broadcast messages
# udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_client_socket.bind(('', 8889))
# udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#
# # Listen for the UDP broadcast message
# print("Waiting for UDP broadcast message...")
# while True:
#     data, server_address = udp_client_socket.recvfrom(1024)
#     message = data.decode('utf-8')
#     if message == BROADCAST_MESSAGE:
#         print("Received UDP broadcast message:", message)
#         break
#
# # Close the UDP socket
# udp_client_socket.close()
#
# # Create a TCP socket and connect to the server
# tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_client_socket.connect(TCP_SERVER_ADDRESS)
# print("Connected to TCP server.")
#
# # Send data over TCP if needed
# # After connecting to the TCP server
# # Receive questions from the server and send answers
# for _ in range(3):  # Assuming there are 3 questions
#     # Receive question from the server
#     question = tcp_client_socket.recv(1024).decode('utf-8')
#     print(f"Received question from server: {question}")
#
#     # Get answer from the user (assuming Y or N)
#     answer = input("Your answer (Y/N): ")
#
#     # Send answer to the server
#     tcp_client_socket.sendall(answer.encode('utf-8'))
#
#     # Receive feedback from the server
#     feedback = tcp_client_socket.recv(1024).decode('utf-8')
#     print(f"Received feedback from server: {feedback}")
#
# # Close the TCP socket
# tcp_client_socket.close()



import socket
import time
import threading
import sys
import select
from random import random


STATE_LOOKING_FOR_SERVER = 0
STATE_CONNECTING_TO_SERVER = 1
STATE_GAME_MODE = 2
class Client:
    def __init__(self):
        self.name = 'Chovav'+'\n' #TODO: randomly pick names
        # Define server address and port for UDP
        self.udp_listen_address = ('0.0.0.0', 13117)
        # Define server address and port for TCP
        #self.tcp_server_address = ('localhost', 8889)
        self.tcp_server_address = None
        # Define client states
        self.state = STATE_LOOKING_FOR_SERVER
        # Define TCP socket
        self.tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.MAGIC_COOKIE = 0xabcddcba.to_bytes(4, byteorder='big')


    # Function to handle state: Looking for a server
    def state_looking_for_server(self):
        udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_client_socket.bind(self.udp_listen_address)
        udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        print("Looking for server...")
        while True:
            data, server_address = udp_client_socket.recvfrom(1024)
            magic_cookie = data[:4]
            message_type = data[4]
            if magic_cookie == self.MAGIC_COOKIE and message_type == 2:
                server_name = data[5:37].decode('utf-8').strip()
                tcp_port = int.from_bytes(data[37:], byteorder='big')
                print("Received offer from server:", server_name)
                print("Server address:", server_address[0])
                print("TCP port:", tcp_port)
                print("Attempting to connect...")
                self.tcp_server_address = (server_address[0], tcp_port)
                udp_client_socket.close()
                return STATE_CONNECTING_TO_SERVER


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

    # Function to handle state: Game mode
    def game_mode(self):
        print("Entering game mode...")
        while True:
            try:
                # Receive question from the server
                question = self.tcp_client_socket.recv(1024).decode('utf-8')
                if not question:
                    print("Connection closed by server.")
                    # Close the TCP socket
                    self.tcp_client_socket.close()
                    return STATE_LOOKING_FOR_SERVER

                print(question)
                # Get answer from the user
                answer = input("Your answer: ")

                # Send answer to the server
                self.tcp_client_socket.sendall(answer.encode('utf-8'))

                # Receive feedback from the server
                feedback = self.tcp_client_socket.recv(1024).decode('utf-8')
                print("Feedback from server:", feedback)

            except Exception as e:
                print("Error:", e)
                # Close the TCP socket
                self.tcp_client_socket.close()
                return STATE_LOOKING_FOR_SERVER


    # Main function to run the client
    def run_client(self):
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


# import socket
# import time
#
# # Define server address and port for UDP
# UDP_SERVER_ADDRESS = ('<broadcast>', 8889)
#
# # Define server address and port for TCP
# TCP_SERVER_ADDRESS = ('localhost', 8889)
#
# # Define the UDP broadcast message
# BROADCAST_MESSAGE = "Hello, this is the server!"
#
# # Function to receive UDP broadcast message
# def receive_udp_broadcast():
#     udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     udp_client_socket.bind(('0.0.0.0', 8889))
#     udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#
#     while True:
#         data, server_address = udp_client_socket.recvfrom(1024)
#         message = data.decode('utf-8')
#         if message == BROADCAST_MESSAGE:
#             print("Received UDP broadcast message:", message)
#             udp_client_socket.close()
#             return
#
# # Create a TCP socket and connect to the server
# def connect_tcp_server():
#     tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcp_client_socket.connect(TCP_SERVER_ADDRESS)
#     print("Connected to TCP server.")
#     return tcp_client_socket
#
# # Receive UDP broadcast message
# receive_udp_broadcast()
# start = time.time()
# tcp_client_socket = connect_tcp_server()
#
# while time.time() - start < 10:
#     message = None
#     message = tcp_client_socket.recv(1024).decode('utf-8')
#     if message is not None:
#         print("Received {answer}".format(answer=message))
#         answer= input("Your answer: ")
#         tcp_client_socket.send(answer.encode('utf-8'))
#     # Connect to TCP server
#
# # Send data over TCP if needed
# #     tcp_client_socket.sendall(b'Hello, TCP server!')
#
# # Close the TCP socket
# tcp_client_socket.close()
