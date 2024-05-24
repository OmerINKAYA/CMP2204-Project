# README.md

## Program Description

This program is a chat application that allows users to communicate with each other over a network. It is written in Python and uses both TCP and UDP protocols for communication. The program consists of four main components:

1. `UDP_Server.py`: This script is responsible for discovering other peers on the network. It listens for broadcast messages from other peers and maintains a list of active users.

2. `UDP_Client.py`: This script broadcasts the user's presence on the network. It periodically sends out a broadcast message containing the user's username.

3. `TCP_Client.py`: This script is used to initiate a chat with another user. It allows the user to choose a recipient from the list of active users, enter a message, and send it to the recipient. The script also supports Diffie-Hellman encryption for secure communication.

4. `TCP_Server.py`: This script listens for incoming chat messages. When a message is received, it is displayed to the user. If the message is encrypted, the script will decrypt it before displaying.

## How to Use

1. Run `UDP_Client.py` to announce your presence on the network.
2. Run `UDP_Server.py` to discover other active users.
3. Run `TCP_Client.py` to send a message to another user encrypted or not and show chat history.
4. Run `TCP_Server.py` to receive messages from other users.

## Known Limitations

1. The program does not support group chats. You can only send a message to one user at a time.
2. The program does not have a graphical user interface. All interactions are done through the command line.
3. The program does not support file transfers. You can only send text messages.
4. The program does not have any form of user authentication. Anyone on the network can use any username they want.
5. The program does not handle network errors gracefully. If there is a problem with the network, the program may crash or behave unpredictably.
