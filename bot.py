from socket import socket

from client import Client
import random
# from faker import Faker

from client import STATE_LOOKING_FOR_SERVER, STATE_CONNECTING_TO_SERVER, STATE_GAME_MODE
class Bot(Client):
    def __init__(self):
        super().__init__()
        self.name = "amit" + "_Bot"

    def choose_answer(self):
        return random.choice(["Y", "N"])

    # def connect_to_server(self, server_address, server_port):
    #     tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     try:
    #         tcp_client_socket.connect((server_address, server_port))
    #         print("Connected to server as bot.")
    #         # Send bot name
    #         bot_name = f"BOT:{random.randint(1000,9999)}"
    #         tcp_client_socket.sendall(bot_name.encode('utf-8') + b'\n')
    #         # Implement bot logic here
    #     except Exception as e:
    #         print(f"Failed to connect to server as bot: {e}")
    #     finally:
    #         tcp_client_socket.close()

    # def bot_mode(self):
    #     print("Entering bot mode...")
    #     while True:
    #         if self.state == STATE_GAME_MODE:
    #             try:
    #                 message = self.bot.generate_message()
    #                 self.tcp_client_socket.sendall(message.encode('utf-8'))
    #             except Exception as e:
    #                 print("Error while sending message:", e)
    #         else:
    #             time.sleep(1)

    def get_messages_from_server(self):
        while True:
            try:
                message = self.tcp_client_socket.recv(1024).decode('utf-8')
                self.send_ans()
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

    def run_client(self):
        while True:  # TODO: CHANGE IT TO DIFFERENT CONDITION
            if self.state == STATE_LOOKING_FOR_SERVER:
                self.state = self.state_looking_for_server()
            elif self.state == STATE_CONNECTING_TO_SERVER:
                self.state = self.state_connecting_to_server()
            elif self.state == STATE_GAME_MODE:
                self.game_mode()

    def send_ans(self):
        try:
            bot_answer = self.choose_answer()
            self.tcp_client_socket.sendall(bot_answer.encode('utf-8'))
        except Exception as e:
            print("Error while sending random choice:", e)


# Create an instance of the GameClient class and run the client
if __name__ == "__main__":
    bot = Bot()
    bot.run_client()