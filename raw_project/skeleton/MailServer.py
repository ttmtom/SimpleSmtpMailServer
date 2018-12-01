#!/usr/bin/python3

from socket import *
import threading
from SMTPConnection import SMTPConnection

# Set the address to localhost, and port number to 1111
HOST = '127.0.0.1'
PORT = 1111
ADDR = (HOST, PORT)
if __name__ == '__main__':
    # Establish the listening socket.
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)

    # Process SMTP client requests in an infinite loop.
    while 1:
        # Listen for a TCP connection request.
        print('waiting for connection...')
        clientsock, addr = serversock.accept()

        # Create a new thread to process the request and start the thread.
        print('...connected from:', addr)
        connection = SMTPConnection(clientsock, addr)
        connection.start()
