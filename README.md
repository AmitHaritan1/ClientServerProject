# Trivia Game Server and Client 🎗️

## Overview
This project consists of a trivia game server and two types of clients: a human client and a bot client. The server hosts a trivia game where players can connect to participate in answering true or false questions. The human client allows users to connect to the server and interactively answer questions, while the bot client automatically generates random answers.

## Files
- **server.py**: Contains the implementation of the trivia game server.
- **client.py**: Contains the implementation of the human client.
- **bot.py**: Contains the implementation of the bot client.

## How to Run
1. Start the server by running `server.py`.
2. Start the human client by running `client.py`.
3. Start the bot client by running `bot.py`.

## Server
The server hosts the trivia game, manages client connections, and handles the game logic. It communicates with clients over TCP/IP sockets.

### Features
- Sends broadcast messages to advertise the server.
- Manages client connections.
- Implements game logic, including asking questions, receiving answers, determining winners, and calculating statistics.

## Client
The client connects to the server and allows players to participate in the trivia game.

### Human Client
- Connects to the server and prompts the user to enter answers to trivia questions.
- Provides interactive gameplay experience.

### Bot Client
- Connects to the server and automatically generates random answers to trivia questions.
- Simulates gameplay without human interaction.

## Dependencies
- Python 3.x
- Standard Python libraries (socket, threading, time)

## Usage
- Ensure that Python 3.x is installed on your system.
- Run the server and clients from the command line using Python.

## For Fun 🎉
Thanks for taking the time to explore our project! Before you go, here's a little something to lighten the mood:

"Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25!" 🎃🎄

We hope that brought a smile to your face 😊 Happy coding!