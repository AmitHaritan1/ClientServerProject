# import socket
#
# # Define server address and port
# SERVER_ADDRESS = ('localhost', 8888)
#
# # Create a UDP socket
# udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # Bind the socket to the server address and port
# udp_server_socket.bind(SERVER_ADDRESS)
# print("UDP server is listening...")
#
# while True:
#     try:
#         # Receive data from the client
#         data, client_address = udp_server_socket.recvfrom(1024)
#         print(f"Received data from {client_address}: {data.decode('utf-8')}")
#
#         # Process the data (for trivia game, you'd ask a question here)
#         response = "What's your answer?"
#
#         # Send response back to the client
#         udp_server_socket.sendto(response.encode('utf-8'), client_address)
#     except ConnectionResetError as e:
#         print(f"ConnectionResetError: {e}")
#         # Continue listening for incoming connections
#         continue
#     except Exception as e:
#         print(f"Error: {e}")
#         # Handle other exceptions as needed
#

## try 2

# import socket
# import time
#
# # Define server address and port
# SERVER_ADDRESS = ('localhost', 8888)
#
# # Define trivia questions and answers
# TRIVIA = [
#     ("What is the capital of France?", "Paris"),
#     ("What is the largest planet in our solar system?", "Jupiter"),
#     ("What is the chemical symbol for water?", "H2O")
# ]
#
# # Create a UDP socket
# udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # Bind the socket to the server address and port
# udp_server_socket.bind(SERVER_ADDRESS)
# print("UDP server is listening...")
#
# # Main loop
# for question, answer in TRIVIA:
#     try:
#         # Send question to the client
#         udp_server_socket.sendto(question.encode('utf-8'), ('localhost', 8888))
#         time.sleep(3)
#         # Receive answer from the client
#         data, client_address = udp_server_socket.recvfrom(1024)
#         client_answer = data.decode('utf-8').strip().lower()
#
#         # Check if the answer is correct
#         if client_answer == answer.lower():
#             feedback = "Correct!"
#         else:
#             feedback = f"Wrong! The correct answer is: {answer}"
#
#         # Send feedback to the client
#         udp_server_socket.sendto(feedback.encode('utf-8'), client_address)
#
#     except Exception as e:
#         print(f"Error: {e}")
#
# # Close the socket
# udp_server_socket.close()

#
# import socket
# import threading
# import time
#
# # Global variables
# CLIENT_CONNECTED = False
#
# # Define server address and port
# UDP_SERVER_ADDRESS = ('', 8888)
# TCP_SERVER_ADDRESS = ('', 8889)
#
# # Define the broadcast message
# BROADCAST_MESSAGE = "Hello, this is the server!"
#
# # Define a list of yes or no questions and correct answers
# YES_NO_QUESTIONS = [
#     ("Is Paris the capital of France?", "Y"),
#     ("Is Jupiter the largest planet in our solar system?", "Y"),
#     ("Is the chemical symbol for water H2O?", "Y")
# ]
#
# # Function to handle UDP broadcast
# def send_broadcast():
#     udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#     while not CLIENT_CONNECTED:
#         udp_server_socket.sendto(BROADCAST_MESSAGE.encode('utf-8'), ('<broadcast>', 8889))
#         print("Broadcast message sent.")
#         time.sleep(1)
#     udp_server_socket.close()
#
# # Function to handle TCP connection
# def handle_tcp_connection():
#     global CLIENT_CONNECTED
#     tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcp_server_socket.bind(TCP_SERVER_ADDRESS)
#     tcp_server_socket.listen(1)  # Listen for just one client
#     print("TCP server started, waiting for a client to connect...")
#     client_socket, client_address = tcp_server_socket.accept()
#     print(f"Connection established with client: {client_address}")
#     CLIENT_CONNECTED = True  # Set flag to indicate client connection
#     # while True:
#     #     # Receive data from the client
#     #     data = client_socket.recv(1024).decode('utf-8')
#     #     if not data:
#     #         break
#     #     print(f"Received from client: {data}")
#     #     masage_back = "hello TCP client!"
#     #     # Send data back to the client
#     #     client_socket.sendall(masage_back.encode('utf-8'))
#     # You can add logic here to handle communication with the client over TCP
#
#     # After the client connection is established
#     for question, correct_answer in YES_NO_QUESTIONS:
#         # Ask a question
#         client_socket.sendall(question.encode('utf-8'))
#
#         # Receive answer from the client
#         answer = client_socket.recv(1024).decode('utf-8')
#         print(f"Received answer from client: {answer}")
#
#         # Check if the answer is correct
#         if answer.strip().lower() == correct_answer.lower():
#             feedback = "Correct!"
#         else:
#             feedback = "Wrong!"
#
#         # Send feedback to the client
#         client_socket.sendall(feedback.encode('utf-8'))
#
#     # Send feedback to the client
#     client_socket.sendall(feedback.encode('utf-8'))
#
#     client_socket.close()
#     tcp_server_socket.close()
#
# # Start a thread for UDP broadcast
# udp_thread = threading.Thread(target=send_broadcast)
# udp_thread.start()
#
# # Start TCP server
# handle_tcp_connection()
#
#




import socket
import threading
import time

# Global variable
CLIENTS = []

# Define server address and port
UDP_SERVER_ADDRESS = ('', 8888)
TCP_SERVER_ADDRESS = ('', 8889)

# Define the broadcast message
BROADCAST_MESSAGE = "Hello, this is the server!"

# Define a list of yes or no questions and correct answers
YES_NO_QUESTIONS = [
    ("Is Paris the capital of France?", "Y"),
    ("Is Jupiter the largest planet in our solar system?", "Y"),
    ("Is the chemical symbol for water H2O?", "Y")
]

# Function to handle UDP broadcast
def send_broadcast():
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while not CLIENTS:
        udp_server_socket.sendto(BROADCAST_MESSAGE.encode('utf-8'), ('<broadcast>', 8889))
        print("Broadcast message sent.")
        time.sleep(1)
    udp_server_socket.close()

# Function to handle TCP connection
def handle_tcp_connection():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(TCP_SERVER_ADDRESS)
    tcp_server_socket.listen(5)  # Listen for up to 5 clients

    print("TCP server started, waiting for clients...")

    while True:
        try:
            client_socket, client_address = tcp_server_socket.accept()
            print(f"Connection established with client: {client_address}")
            CLIENTS.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
        except Exception as e:
            print(f"Error: {e}")

    tcp_server_socket.close()

# Function to handle client communication
def handle_client(client_socket):
    for question, correct_answer in YES_NO_QUESTIONS:
        try:
            # Ask a question
            client_socket.sendall(question.encode('utf-8'))

            # Receive answer from the client
            answer = client_socket.recv(1024).decode('utf-8')
            print(f"Received answer from client: {answer}")

            # Check if the answer is correct
            if answer.strip().lower() == correct_answer.lower():
                feedback = "Correct!"
            else:
                feedback = "Wrong!"

            # Send feedback to the client
            client_socket.sendall(feedback.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

# Start a thread for UDP broadcast
udp_thread = threading.Thread(target=send_broadcast)
udp_thread.start()

# Start TCP server
handle_tcp_connection()
