#!/bin/python3
import socket
import threading
import logging

# Connection Data
host = '46.151.28.196'
port = 55555

# Logger
file_log = logging.FileHandler('Log.log')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), 
                    format='[%(asctime)s | %(levelname)s]: %(message)s', 
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    index = clients.index(client)
    nickname = nicknames[index]
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode("ascii")
            message_with_reciever = "{}: {}".format(nickname, message).encode("ascii")
            broadcast(message_with_reciever)
            logging.info(message_with_reciever.decode("ascii"))            
        except Exception as e:
            # Removing And Closing Clients            
            clients.remove(client)
            client.close()
            info = "{} left!".format(nickname).encode('ascii')         
            broadcast(info)
            logging.info(e)
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        try:
            # Accept Connection
            client, address = server.accept()
            logging.info("Connected with {}".format(str(address)))

            # Request And Store Nickname
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            # Print And Broadcast Nickname
            logging.info("Nickname is {}".format(nickname))
            broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            logging.critical(e)
            break


logging.info("Server if listening...")
receive()
