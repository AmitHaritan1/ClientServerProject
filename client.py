import socket
import time
import threading
import sys
import select
from random import random
from random import choice
import msvcrt


STATE_LOOKING_FOR_SERVER = 0
STATE_CONNECTING_TO_SERVER = 1
STATE_GAME_MODE = 2
entertaining_names = [
"Moshe Ya'alon", 'Gad Elbaz', 'Doron Ben-David', 'Dana International', 'Yaakov Litzman',
 'Shlomo Artzi', 'Lior Raz', 'Yigal Allon', 'Eyal Golan', 'Meir Dagan', 'Bar Refaeli',
 'Shiri Maimon', 'Ben-Gurion', 'Yair Lapid', 'Rotem Sela', 'Gal Gadot', 'Yitzhak Rabin',
 'Naftali Bennett', 'Natan Sharansky', 'Natalie Portman', 'Omer Adam', 'Tamar Zandberg',
 'Amir Peretz', 'Itay Tiran', 'Moshe Dayan', 'Tzipi Livni', 'Orphaned Land', 'Netta Barzilai',
 'Menachem Begin', 'Yitzhak Mordechai', 'Yisrael Katz', 'Avigdor Lieberman', 'Aryeh Deri',
 'Yael Grobglas', 'Yotam Ottolenghi', 'David Ben-Gurion', 'Benjamin Netanyahu', 'Yuval Dayan',
 'Adva Dadon', 'Shulamit Aloni', 'Yuli Edelstein', 'Yitzhak Shamir', 'Levi Eshkol', 'Rafi Eitan',
 'Theodor Herzl', 'Benny Gantz', 'Moshe Sharett', 'Golda Meir', 'Ezer Weizman', 'Yehuda Poliker',
 'Idan Raichel', 'David Levy', 'Bezalel Smotrich', 'Zehava Galon', 'Ayman Odeh', 'Odeya',
 'Sacha Baron Cohen', 'Yael Naim', 'Reuven Rivlin', 'Benny Begin', 'Ayelet Zurer', 'Ehud Barak',
 "Gideon Sa'ar", 'Avi Gabbay', 'Ariel Sharon', 'Shimon Peres', 'Danny Danon', 'Ahmed Tibi',
 'Uri Ariel', 'Eliezer Ben-Yehuda'
]

class Player:
    def __init__(self):
        print("Client started, listening for offer requests")
        self.name = choice(entertaining_names) + '\n'  # randomly pick a name from the list
        # Define server address and port for UDP
        self.udp_listen_address = ('0.0.0.0', 13117)
        self.tcp_server_address = None
        # Define client states
        self.state = STATE_LOOKING_FOR_SERVER
        # Define TCP socket
        self.MAGIC_COOKIE = 0xabcddcba.to_bytes(4, byteorder='big')
        self.tcp_client_socket = None
        self.waiting_for_input = False

    def _state_looking_for_server(self):
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
                print(f"Received offer from server \"{server_name}\" at address {server_address[0]}, attempting to connect...")
                self.tcp_server_address = (server_address[0], tcp_port)
                udp_client_socket.close()
                self.tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                return STATE_CONNECTING_TO_SERVER
            time.sleep(1)

    # Function to handle state: Connecting to a server
    def _state_connecting_to_server(self):
        try:
            self.tcp_client_socket.connect(self.tcp_server_address)
            self.tcp_client_socket.sendall(self.name.encode('utf-8'))
            print("Connected to TCP server.")
            return STATE_GAME_MODE
        except Exception as e:
            print("Failed to connect to server:", e)
            return STATE_LOOKING_FOR_SERVER

    def _get_messages_from_server(self):
        while True:
            try:
                message = self.tcp_client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                else:
                    print(message)
            except ConnectionResetError as e:
                break

            except Exception as e:
                print("Error while getting message from the server:", e)
                break

        # Close the TCP socket
        print("Server disconnected, listening for offer requests...")
        self.tcp_client_socket.close()
        self.state = STATE_LOOKING_FOR_SERVER


    # Function to handle state: Game mode
    def _game_mode(self):
        print("Entering game mode...")
        listen_thread = threading.Thread(target=self._get_messages_from_server)
        listen_thread.start()
        listen_thread.join()




class Client(Player):
    def __init__(self):
        super().__init__()

    # # Function to handle state: Looking for a server
    # def _state_looking_for_server(self):
    #     udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     udp_client_socket.bind(self.udp_listen_address)
    #     udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #
    #     while True: #TODO: consider changing the condition or adding sleep
    #         data, server_address = udp_client_socket.recvfrom(1024)
    #         magic_cookie = data[:4]
    #         message_type = data[4]
    #         if magic_cookie == self.MAGIC_COOKIE and message_type == 2:
    #             server_name = data[5:37].decode('utf-8').strip()
    #             tcp_port = int.from_bytes(data[37:], byteorder='big')
    #             print(f"Received offer from server \"{server_name}\" at address {server_address[0]}, attempting to connect...")
    #             self.tcp_server_address = (server_address[0], tcp_port)
    #             udp_client_socket.close()
    #             self.tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             return STATE_CONNECTING_TO_SERVER
    #         time.sleep(1)


    # Function to handle state: Connecting to a server
    # def _state_connecting_to_server(self):
    #     try:
    #         self.tcp_client_socket.connect(self.tcp_server_address)
    #         self.tcp_client_socket.sendall(self.name.encode('utf-8'))
    #         print("Connected to TCP server.")
    #         return STATE_GAME_MODE
    #     except Exception as e:
    #         print("Failed to connect to server:", e)
    #         return STATE_LOOKING_FOR_SERVER

    # def _get_messages_from_server(self):
    #     while True:
    #         try:
    #             message = self.tcp_client_socket.recv(1024).decode('utf-8')
    #             if not message:
    #                 print("Server disconnected, listening for offer requests...")
    #                 self.tcp_client_socket.close()
    #                 self.state = STATE_LOOKING_FOR_SERVER
    #                 break
    #             else:
    #                 print(message)
    #         except Exception as e:
    #             print("Error while getting message from the server:", e)
    #             # Close the TCP socket
    #             #self.tcp_client_socket.close()

    def _get_user_input(self):
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
    # def _game_mode(self):
    #     print("Entering game mode...")
    #     listen_thread = threading.Thread(target=self._get_messages_from_server)
    #     listen_thread.start()
    #     listen_thread.join()

    # Main function to run the client
    def run_client(self):
        keyboard_thread = threading.Thread(target=self._get_user_input)
        keyboard_thread.start()
        while True:  # TODO: CHANGE IT TO DIFFERENT CONDITION
            if self.state == STATE_LOOKING_FOR_SERVER:
                self.state = self._state_looking_for_server()
            elif self.state == STATE_CONNECTING_TO_SERVER:
                self.state = self._state_connecting_to_server()
            elif self.state == STATE_GAME_MODE:
                self._game_mode()



# Create an instance of the GameClient class and run the client
if __name__ == "__main__":
    client = Client()
    client.run_client()