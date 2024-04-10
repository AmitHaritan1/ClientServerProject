import socket
import threading
import time
from random import shuffle
import subprocess


class Server:
    def __init__(self):
        self.udp_port = 13117
        self.tcp_port = 0
        self.MAGIC_COOKIE = 0xabcddcba.to_bytes(4, byteorder='big')
        self.server_name = "The best trivia server ever"
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.offer_message = ''

        def wlan_ip():
            result = subprocess.run('ipconfig', stdout=subprocess.PIPE, text=True).stdout.lower()
            scan = 0
            for i in result.split('\n'):
                if 'wireless' in i:
                    scan = 1
                if scan:
                    if 'ipv4' in i:
                        return i.split(':')[1].strip()
        self.ip_address = wlan_ip()
        # Global variables
        self.clients = {}
        self.last_client_join_time = 0
        self.game_mode = False
        self.client_answers = {}
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
    def send_offer(self):
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

    def handle_tcp_connection(self):
        while not self.game_mode:
            try:
                client_socket, client_address = self.tcp_server_socket.accept()
                self.last_client_join_time = time.time()
                client_socket.setblocking(False)
                print(f"Connection established with client: {client_address}")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except socket.error as e:
                time.sleep(1)
        # TODO: think what do we want to do with clients connecting to the server once the game started

    # Function to handle individual client
    def handle_client(self, client_socket):
        try:
            player_name = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Player {player_name} connected.")
            self.clients[client_socket]=player_name
            # Implement game logic here
            # TODO: make sure that someone starts the game
            # TODO: make sure to close the client socket when the game is over
            #client_socket.close()
        except Exception as e:
            print(f"Error handling client: {e}")

    def next_question(self):
        if self.current_question_index < len(self.trivia_questions):
            question, answer = self.trivia_questions[self.current_question_index]
            self.current_question_index += 1
            if answer == 'Y':
                correct_answer = ['Y', 'T', 1]
            else:
                correct_answer = ['N', 'F', 0]
            return question, correct_answer
        else: # No more questions available
            shuffle(self.trivia_questions)
            self.current_question_index = 0
            return self.next_question()

    def start_timer(self, start_time):
        while time.time() - start_time < 10 and len(self.client_answers) < len(self.clients):
            time.sleep(1)

    def print_round(self, game_round):
        names = list(self.clients.values())
        if len(names) > 1:
            result = ', '.join(names[:-1]) + ' and ' + names[-1]
        else:
            result = names[0]
        print(f"Round {game_round}, played by {result}:")

    def send_to_all_clients(self, message):
        for client_socket in self.clients.keys():
            try:
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                player_name = self.clients[client_socket]
                print(f"Error while sending info to client {player_name}: {e}")

    def welcome_message(self):
        welcome = f"Welcome to the \"{self.server_name}\" server, where we are answering intriguing trivia questions!"
        for i, name in enumerate(self.clients.values()):
            welcome += f"\nPlayer {i+1}: {name}"
        print(welcome)
        self.send_to_all_clients(welcome)
        end = "="*30
        print(end)
        for client_socket, client_name in self.clients.items():
            try:
                message = "You are playing as " + client_name + ", good luck!\n"
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error while sending welcome to client {client_name}: {e}")
        self.send_to_all_clients(end+'\n')


    # Function to start the game
    def start_game(self):
        self.welcome_message()
        shuffle(self.trivia_questions)
        game_round = 0
        while self.clients:
            question, correct_answer = self.next_question()
            game_round += 1
            self.print_round(game_round)
            question = f"True or False: {question}"
            print(question)
            try:
                self.send_to_all_clients(question)
                # answer_threads = []
                # for client_socket in self.clients.keys():
                #     answer_thread = threading.Thread(target=self.receive_answer, args=(question, client_socket,))
                #     answer_threads.append(answer_thread)
                #     answer_thread.start()
                # Start a timer for 10 seconds
                # timer_thread = threading.Thread(target=self.start_timer, args=(time.time(),))
                # timer_thread.start()
                # timer_thread.join()
                time.sleep(10)
                for client_socket in self.clients.keys():
                    try:
                        answer = client_socket.recv(1024).decode('utf-8').strip()
                        self.client_answers[client_socket] = answer
                    except socket.error as e:
                        # no answer from client
                        print(e)
                        self.client_answers[client_socket] = 'Z'
                for client_socket, answer in self.client_answers.items():
                    player_name = self.clients[client_socket]
                    feedback = True if answer in correct_answer else False
                    if feedback:
                        client_message = "You are correct!"
                        server_message = f"{player_name} is correct!"
                    else:
                        client_message= "You are incorrect!"
                        server_message = f"{player_name} is incorrect!"
                    client_socket.sendall(client_message.encode('utf-8'))
                    print(server_message)

                # If not all clients answered the wrong question - remove all the clients that answered wrong
                correct_clients = [client_socket for client_socket, answer in self.client_answers.items() if answer in correct_answer]
                looseres = []
                if len(correct_clients) == 1:  # if we found our winner
                    winner_name = self.clients[correct_clients[0]]
                    print(f"{winner_name} wins!")
                    self.send_to_all_clients(f"{winner_name} wins!\n")
                    print("Game over!")
                    self.send_to_all_clients("Game over!\n")
                    print(f"Congratulations to the winner: {winner_name}")
                    self.send_to_all_clients(f"Congratulations to the winner: {winner_name}\n")
                    print("Game over, sending out offer requests...")
                    looseres = list(self.clients.keys())
                elif len(correct_clients) > 1 and len(correct_clients) != len(self.clients):
                    for client_socket, answer in self.client_answers.items():
                        if answer not in correct_answer:
                            client_socket.sendall("You lost - Game over!".encode('utf-8'))
                            looseres.append(client_socket)
                for client_socket in looseres:
                    del self.clients[client_socket]
                    client_socket.close()
                self.client_answers = {}
            except Exception as e:
                #print(e.with_traceback())
                print(f"Error handling game logic: {e}")
                #break
        self.tcp_server_socket.close()
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_port = 0
        self.client_answers = {}
        self.game_mode = False
        self.current_question_index = 0


    # Function to receive answer from a client
    def receive_answer(self, question, client_socket):
        answer = client_socket.recv(1024).decode('utf-8').strip()
        while answer not in ['Y','T','N','F',0,1]:
            client_socket.sendall(self.invalid_answer_message.encode('utf-8'))
            client_socket.sendall(question.encode('utf-8'))
            answer = client_socket.recv(1024).decode('utf-8').strip()
        self.client_answers[client_socket] = answer

    # Main function to start the server
    def start_server(self):

        print(f"server started, listening on IP address {self.ip_address}")
        while True:
            self.tcp_server_socket.bind(('', self.tcp_port))
            self.tcp_port = self.tcp_server_socket.getsockname()[1]
            self.tcp_server_socket.setblocking(False)  # Set non-blocking mode
            self.tcp_server_socket.listen()
            tcp_thread = threading.Thread(target=self.handle_tcp_connection)
            tcp_thread.start()
            udp_thread = threading.Thread(target=self.send_offer)
            udp_thread.start()
            udp_thread.join()
            tcp_thread.join()
            self.start_game()



# Create an instance of the GameServer class and start the server
if __name__ == "__main__":
    server = Server()
    server.start_server()
