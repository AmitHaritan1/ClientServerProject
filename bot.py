from client import Client
from random import random
from faker import Faker


class Bot(Client):
    def __init__(self):
        super().__init__()
        self.name = Faker().first_name() + "_Bot"

    def choose_answer(self):
        return random.choice(["Y", "N"])

    def connect_to_server(self, server_address, server_port):
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client_socket.connect((server_address, server_port))
            print("Connected to server as bot.")
            # Send bot name
            bot_name = f"BOT:{random.randint(1000,9999)}"
            tcp_client_socket.sendall(bot_name.encode('utf-8') + b'\n')
            # Implement bot logic here
        except Exception as e:
            print(f"Failed to connect to server as bot: {e}")
        finally:
            tcp_client_socket.close()