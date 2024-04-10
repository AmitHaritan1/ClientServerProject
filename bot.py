from socket import socket

from client import Client
import random

from client import STATE_LOOKING_FOR_SERVER, STATE_CONNECTING_TO_SERVER, STATE_GAME_MODE


class Bot(Client):
    def __init__(self):
        super().__init__()
        self.name = "BOT " + self.name

    def _choose_answer(self):
        return random.choice(["Y", "N"])

    def _get_messages_from_server(self):
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
                    if message[:14] == 'True or False:': self.send_ans()
            except Exception as e:
                print("Error while getting message from the server:", e)
                # Close the TCP socket
                # self.tcp_client_socket.close()

    def run_bot(self):
        while True:  # TODO: CHANGE IT TO DIFFERENT CONDITION
            if self.state == STATE_LOOKING_FOR_SERVER:
                self.state = self._state_looking_for_server()
            elif self.state == STATE_CONNECTING_TO_SERVER:
                self.state = self._state_connecting_to_server()
            elif self.state == STATE_GAME_MODE:
                self._game_mode()

    def send_ans(self):
        try:
            bot_answer = self._choose_answer()
            self.tcp_client_socket.sendall(bot_answer.encode('utf-8'))
        except Exception as e:
            print("Error while sending random choice:", e)


# Create an instance of the GameClient class and run the client
if __name__ == "__main__":
    bot = Bot()
    bot.run_bot()
