import socket
import threading
import time
from random import shuffle


# ANSI color codes
# Defining ANSI color codes for better console output readability
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
PINK = '\033[95m'


# ANSI text style codes
# Defining ANSI text style codes for better console output readability
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ITALIC = '\033[3m'

class Server:
    def __init__(self):
        # Initialize server settings and variables
        self.udp_port = 13117  # UDP port for broadcasting server offer message
        self.tcp_port = 0  # TCP port for handling client connections
        self.MAGIC_COOKIE = 0xabcddcba.to_bytes(4, byteorder='big')  # Magic cookie for server identification
        self.server_name = "The best trivia server ever"
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.offer_message = ''
        self.ip_address = socket.gethostbyname(socket.gethostname())
        # Global variables
        self.clients = {}  # Dictionary to store connected clients
        self.last_client_join_time = 0  # Timestamp for the last client connection
        self.game_mode = False  # Flag indicating whether the game is in progress
        self.client_scores = {}
        self.client_answers = {}
        self.legal_answers = ['Y', 'T', '1', 'N', 'F', '0']
        self.answer_uses = {answer:0 for answer in self.legal_answers}
        self.answer_uses['illegal'] = 0
        self.answer_uses['no answer'] = 0
        self.global_answer_uses = self.answer_uses
        self.all_time_wins = {}
        # Define a list of yes or no questions and correct answers
        self.trivia_questions = [
            ("Is Paris the capital of France?", "Y"),
            ("Is Jupiter the largest planet in our solar system?", "Y"),
            ("Is the chemical symbol for water H2O?", "Y"),
            ("Is the Great Wall of China visible from space?", "N"),
            ("Is the Mona Lisa painting displayed in the Louvre Museum?", "Y"),
            ("Is the Earth the third planet from the Sun?", "Y"),
            ("Is Mount Everest the tallest mountain on Earth?", "Y"),
            ("Is the Amazon River the longest river in the world?", "Y"),
            ("Is the Eiffel Tower located in London?", "N"),
            ("Is the speed of light faster than the speed of sound?", "Y"),
            ("Is the Statue of Liberty located in Paris?", "N"),
            ("Is a tomato a fruit?", "Y"),
            ("Is Antarctica the largest continent on Earth?", "N"),
            ("Is the moon bigger than the Earth?", "N"),
            ("Is the sun a planet?", "N"),
            ("Is the Pythagorean theorem related to triangles?", "Y"),
            ("Is the Big Ben clock located in Paris?", "N"),
            ("Is English the most spoken language in the world?", "N"),
            ("Is the Pacific Ocean the largest ocean on Earth?", "Y"),
            ("Is a cucumber classified as a fruit?", "Y"),
            ("Is the Sahara Desert the largest desert in the world?", "N"),
            ("Is a tomato a vegetable?", "Y"),
            ("Is New York City the capital of the United States?", "N"),
            ("Is the Statue of Liberty a gift from France to the US?", "Y"),
            ("Is the Great Pyramid of Giza one of the Seven Wonders of the World?", "Y"),
            ("Is the Celsius scale used to measure temperature in the US?", "N"),
            ("Is the Amazon Rainforest located in South America?", "Y"),
            ("Is the human heart located on the left side of the body?", "Y"),
            ("Is a rhinoceros a herbivore?", "Y"),
            ("Is a square also a rectangle?", "Y"),
            ("Is the Atlantic Ocean the second largest ocean on Earth?", "Y"),
            ("Is Mount Kilimanjaro the tallest mountain in Africa?", "Y"),
            ("Is a strawberry a type of berry?", "Y"),
            ("Is the capital of Japan Tokyo?", "Y"),
            ("Is the largest mammal on Earth the blue whale?", "Y"),
            ("Is gold a chemical element?", "Y"),
            ("Is the speed of light approximately 300,000 kilometers per second?", "Y"),
            ("Is an octopus an invertebrate?", "Y"),
            ("Is the Nile River the longest river in the world?", "N"),
            ("Is the largest planet in our solar system Jupiter?", "Y"),
            ("Is oxygen the most abundant element in the Earth's atmosphere?", "Y"),
            ("Is the United Kingdom comprised of England, Scotland, and Wales?", "Y"),
            ("Is a panda classified as a bear?", "Y"),
            ("Is the color of the sky usually blue?", "Y"),
            ("Is a butterfly an insect?", "Y"),
            ("Is the Arctic Circle located in the Northern Hemisphere?", "Y"),
            ("Is the Statue of Liberty made of copper?", "Y"),
            ("Is the Taj Mahal located in India?", "Y"),
            ("Is a piano a percussion instrument?", "Y"),
            ("Is the Leaning Tower of Pisa located in Italy?", "Y"),
            ("Is a kangaroo native to Australia?", "Y"),
            ("Is a koala a marsupial?", "Y"),
            ("Is the Pacific Rim known for its seismic activity?", "Y"),
            ("Is the Great Barrier Reef the largest coral reef system in the world?", "Y"),
            ("Is the Statue of Liberty green?", "Y"),
            ("Is a honeybee a pollinator?", "Y"),
            ("Is the Rhine River located in Europe?", "Y"),
            ("Is the Panama Canal a man-made waterway?", "Y"),
            ("Is the Mona Lisa painted by Leonardo da Vinci?", "Y"),
            ("Is the currency of Japan the yen?", "Y"),
            ("Is the Sahara Desert located in Africa?", "Y"),
            ("Is the Arctic Ocean the smallest ocean on Earth?", "Y"),
            ("Is the capital of Australia Canberra?", "Y"),
            ("Is the International Space Station (ISS) orbiting the Earth?", "Y"),
            ("Is a cheetah the fastest land animal?", "Y"),
            ("Is the currency of the United States the dollar?", "Y"),
            ("Is the Mediterranean Sea connected to the Atlantic Ocean?", "Y"),
            ("Is a snail a mollusk?", "Y"),
            ("Is a dolphin a mammal?", "Y"),
            ("Is the Earth's atmosphere composed primarily of nitrogen?", "Y"),
            ("Is the Mona Lisa smiling?", "Y"),
            ("Is the Mariana Trench the deepest part of the world's oceans?", "Y"),
            ("Is the human body made up mostly of water?", "Y"),
            ("Is the Amazon Rainforest home to a diverse range of plant and animal species?", "Y"),
            ("Is the Louvre Museum located in Paris?", "Y"),
            ("Is the capital of Canada Ottawa?", "Y"),
            ("Is the moon illuminated by the sun?", "Y"),
            ("Is the Nile River located in South America?", "N"),
            ("Is the Great Wall of China longer than 10,000 miles?", "Y"),
            ("Is the North Pole colder than the South Pole?", "Y"),
            ("Is a giraffe the tallest living terrestrial animal?", "Y"),
            ("Is the currency of the United Kingdom the euro?", "N"),
            ("Is a tarantula a type of spider?", "Y"),
            ("Is the Big Ben clock tower located in New York City?", "N"),
            ("Is a turtle classified as a reptile?", "Y"),
            ("Is a strawberry a type of berry?", "Y"),
            ("Is a cucumber classified as a fruit?", "Y"),
            ("Is a kangaroo native to Australia?", "Y"),
            ("Is a zebra black with white stripes?", "N"),
            ("Is a tomato a fruit?", "Y"),
            ("Is a potato a root vegetable?", "Y")
        ]
        self.current_question_index = 0
        self.invalid_answer_message = "Invalid answer received. The only valid answers are: Y/T/1 for a True statement, or N/F/0 for a false statement."


    # Function to handle UDP broadcast
    def _send_offer(self):
        """
        Function to send UDP broadcast message with server offer to clients.
        This function runs in a separate thread.
        """
        self.offer_message = (self.MAGIC_COOKIE + b'\x02' + self.server_name.ljust(32).encode('utf-8') +
                              self.tcp_port.to_bytes(2, byteorder='big'))
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while time.time() - self.last_client_join_time < 10 or not self.clients:
            udp_server_socket.sendto(self.offer_message, ('<broadcast>', self.udp_port))
            print("Offer message sent")
            # TODO: drop prints when finished debugging
            time.sleep(1)
        self.game_mode = True
        udp_server_socket.close()

    def _handle_tcp_connection(self):
        while not self.game_mode:
            try:
                client_socket, client_address = self.tcp_server_socket.accept()
                self.last_client_join_time = time.time()
                client_socket.setblocking(False)
                print(f"Connection established with client: {client_address}")
                threading.Thread(target=self._handle_client, args=(client_socket,)).start()
            except socket.error as e:
                time.sleep(1)
        # TODO: think what do we want to do with clients connecting to the server once the game started

    # Function to handle individual client
    def _handle_client(self, client_socket):
        try:
            player_name = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Player {player_name} connected.")
            self.clients[client_socket]=player_name
            self.client_scores[player_name] = 0
            # Implement game logic here
            # TODO: make sure that someone starts the game
            # TODO: make sure to close the client socket when the game is over
            #client_socket.close()
        except Exception as e:
            print(f"Error handling client: {e}")

    def _next_question(self):
        if self.current_question_index < len(self.trivia_questions):
            question, answer = self.trivia_questions[self.current_question_index]
            self.current_question_index += 1
            if answer == 'Y':
                correct_answer = ['Y', 'T', '1']
            else:
                correct_answer = ['N', 'F', '0']
            return question, correct_answer
        else: # No more questions available
            shuffle(self.trivia_questions)
            self.current_question_index = 0
            return self._next_question()

    def _start_timer(self, start_time):
        while time.time() - start_time < 10 and len(self.client_answers) < len(self.clients):
            time.sleep(1)

    def _print_round(self, game_round):
        names = list(self.clients.values())
        if len(names) > 1:
            result = ', '.join(names[:-1]) + ' and ' + names[-1]
        else:
            result = names[0]
        print(f"Round {game_round}, played by {result}:")

    def _send_to_all_clients(self, message):
        client_sockets = list(self.clients.keys())
        for client_socket in client_sockets:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except ConnectionError:
                self._disconnect_client(client_socket)
            except Exception as e:
                #player_name = self.clients[client_socket]
                #print(f"Error while sending info to client {player_name}: {e}")
                print(f"Error while sending info to client: {e}")

    def _welcome_message(self):
        white_background_string = "\033[47m Hello, World! \033[0m"

        welcome = f"🥳🥳🥳 Welcome to the \"{self.server_name}\" server, where we are answering intriguing trivia questions! 🥳🥳🎗️"
        client_names = list(self.clients.values())
        client_sockets = list(self.clients.keys())
        for i, (name, client_socket) in enumerate(zip(client_names, client_sockets)):
            if client_socket in self.clients.keys():
                welcome += f"\nPlayer {i+1}: {name}"
        self._send_to_all_clients(welcome)
        end = "="*30
        client_names = list(self.clients.values())
        client_sockets = list(self.clients.keys())
        for (client_name, client_socket) in zip(client_names, client_sockets):
            try:
                message = "You are playing as " + PINK + client_name + RESET + ", good luck!"
                client_socket.sendall(message.encode('utf-8'))
            except ConnectionError:
                self._disconnect_client(client_socket)
            except socket.error as e:
                print('socket error') #TODO: delete
                self._disconnect_client(client_socket)
            except Exception as e:
                print(f"Error while sending welcome to client {client_name}: {e}")
        if self.clients:
            print(welcome)
            print(end)
        self._send_to_all_clients(end)

    def _disconnect_client(self, client_socket):
        client_name = self.clients.pop(client_socket, None)
        client_socket.close()
        if client_name:
            print(f"Player {client_name} disconnected.")
        self.client_answers.pop(client_socket, None)
        return len(self.clients)

    # Function to start the game
    def _start_game(self):
        self.answer_uses = {answer:0 for answer in self.answer_uses.keys()}
        self._welcome_message()
        shuffle(self.trivia_questions)
        game_round = 0
        winner_name = "NoWinner"  # initialize parameter
        while self.clients:
            question, correct_answer = self._next_question()
            game_round += 1
            self._print_round(game_round)
            question = f"True or False: " + BOLD + f"{question}" + RESET
            print(question)
            try:
                self._send_to_all_clients(question)
                time.sleep(10)
                client_sockets = self.clients.keys()
                for client_socket in client_sockets:
                    try:
                        answer = client_socket.recv(1024).decode('utf-8').strip()
                        if not answer:
                            if self._disconnect_client(client_socket) == 0:
                                print("All players quit, Game over! sending out offer requests...")
                                break
                        else:
                            self.client_answers[client_socket] = answer
                    except socket.error as e:
                        # no answer from client
                        self.client_answers[client_socket] = None
                    except ConnectionError:
                        # client disconnected
                        if self._disconnect_client(client_socket) == 0:
                            print("All players quit, Game over! sending out offer requests...")
                            break
                    except Exception as e:
                        print(f"Error while getting answer from client: {e}")
                client_sockets, client_answers = list(self.client_answers.keys()), list(self.client_answers.values())
                correct_clients = []
                losers = []
                for (client_socket, answer) in zip(client_sockets, client_answers):
                    try:
                        player_name = self.clients.get(client_socket)
                        if not player_name:
                            # client disconnected
                            if self._disconnect_client(client_socket) == 0:
                                print("All players quit, Game over! sending out offer requests...")
                                break
                    except Exception as e:
                        print(f"Error while getting player name: {e}")
                        continue
                    feedback = True if answer in correct_answer else False
                    if answer in self.legal_answers:
                        self.answer_uses[answer] += 1
                    if feedback:
                        client_message = GREEN + "You are correct!" + RESET
                        server_message = GREEN + f"{player_name} is correct!" + RESET
                        correct_clients.append(client_socket)
                        self.client_scores[player_name] += 1
                    else:
                        if answer is None:
                            client_message = RED + "You did not answer in time!" + RESET
                        elif answer not in self.legal_answers:
                            client_message = self.invalid_answer_message
                            self.answer_uses['illegal'] += 1
                        else:
                            client_message = RED + "You are incorrect!" + RESET
                        server_message = RED + f"{player_name} is incorrect!" + RESET
                        losers.append(client_socket)
                    try:
                        client_socket.sendall(client_message.encode('utf-8'))
                    except ConnectionError:
                        if self._disconnect_client(client_socket) == 0:
                            print("All players quit, Game over! sending out offer requests...")
                            break
                    except Exception as a:
                        continue
                    finally:
                        print(server_message)

                if len(correct_clients) == 1:  # if we found our winner
                    winner_name = self.clients.get(correct_clients[0], "disconnected winner")
                    print(f"{winner_name} wins! 🏆")
                    self._send_to_all_clients(f"{winner_name} wins! 🏆")
                    print("Game over!")
                    print(f"Congratulations to the winner: {winner_name}, with {self.client_scores[winner_name]} points! 🎮🎉")
                    self._send_to_all_clients(CYAN + f"Congratulations to the winner: {winner_name}, with {self.client_scores[winner_name]} points!" + RESET)
                    self._send_to_all_clients("Game over!")

                elif len(correct_clients) > 1 and len(correct_clients) != len(self.clients):
                    for client_socket, answer in zip(client_sockets, client_answers):
                        if answer not in correct_answer:
                            try:
                                client_socket.sendall(f"You lost - Game over! 👎 \n In this game you earned {self.client_scores[self.clients[client_socket]]} points".encode('utf-8'))
                                losers.append(client_socket)
                            except ConnectionError:
                                if self._disconnect_client(client_socket) == 0:
                                    print("All players quit, Game over! sending out offer requests...")
                                    break
                            except Exception as a:
                                self._disconnect_client(client_socket)
                if len(losers) != len(self.clients):
                    for client_socket in losers:
                        self._disconnect_client(client_socket)
                    if len(correct_clients) == 1:
                        self._disconnect_client(correct_clients[0])
                self.client_answers = {}
            except Exception as e:
                print(f"Error handling game logic: {e}")
                client_sockets = list(self.clients.keys())
                for client_socket in client_sockets:
                    self._disconnect_client(client_socket)
                break
        self._print_statistics(winner_name)
        self.tcp_server_socket.close()
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_port = 0
        self.client_answers = {}
        self.game_mode = False
        self.current_question_index = 0

    def _print_statistics(self, winner_name):
        # statistics:
        print()
        print(UNDERLINE + BOLD + "Game Statistics:" + RESET)
        for client in self.clients.keys():
            print(str(self.clients[client]) + " : " + str(self.client_scores[self.clients[client]]) + " points")
        print("most common answer in this game: " + max(self.answer_uses, key=self.answer_uses.get))
        self.global_answer_uses = {key: self.global_answer_uses[key] + self.answer_uses[key] for key in
                                   self.global_answer_uses.keys()}
        print("most common answer in all games: " + max(self.global_answer_uses, key=self.global_answer_uses.get))
        if winner_name in self.all_time_wins.keys():
            self.all_time_wins[winner_name] += 1
        else:
            self.all_time_wins[winner_name] = 1
        print("All time wins: " + max(self.all_time_wins, key=self.all_time_wins.get) + " with " + str(
            self.all_time_wins[max(self.all_time_wins, key=self.all_time_wins.get)]) + " wins")
        print(BOLD + "Game over, sending out offer requests..." + RESET)
        print()

    # Main function to start the server
    def start_server(self):

        print(f"server started, listening on IP address {self.ip_address}")
        while True:
            self.tcp_server_socket.bind(('', self.tcp_port))
            self.tcp_port = self.tcp_server_socket.getsockname()[1]
            self.tcp_server_socket.setblocking(False)  # Set non-blocking mode
            self.tcp_server_socket.listen()
            tcp_thread = threading.Thread(target=self._handle_tcp_connection)
            tcp_thread.start()
            udp_thread = threading.Thread(target=self._send_offer)
            udp_thread.start()
            udp_thread.join()
            tcp_thread.join()
            self._start_game()



# Create an instance of the GameServer class and start the server
if __name__ == "__main__":
    server = Server()
    server.start_server()