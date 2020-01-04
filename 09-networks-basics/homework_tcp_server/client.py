import socket
import select
import sys

HEADER_LENGTH = 10
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = "127.0.0.1"
Port = 1234
server.connect((IP_address, Port))
my_username = input("Username: ")


username_current = my_username.encode('utf-8')
username_header = f"{len(username_current):<{HEADER_LENGTH}}".encode('utf-8')
server.send(username_header + username_current)

while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    """ There are two possible input situations. Either the
    user wants to give  manual input to send to other people,
    or the server is sending a message  to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets, write_socket, error_socket =\
        select.select(sockets_list, [], [])

    print('msg: ')
    for socks in read_sockets:

        # Server send message
        if socks == server:
            username_header = server.recv(HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())
            # Receive and decode username
            username = server.recv(username_length).decode('utf-8')
            if username == username_current.decode('utf-8'):
                message_header = server.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = server.recv(message_length).decode('utf-8')
                print(f'{message}')
            else:
                message_header = server.recv(HEADER_LENGTH)
                print("message_header: ", message_header)
                message_length = int(message_header.decode('utf-8').strip())
                message = server.recv(message_length).decode('utf-8')
                print(f'<{username}> {message}')

        # User send message to server
        else:
            message = input()
            print('message: ', message)
            # Exit
            if message.strip() == 'q':
                print('We will miss you')
                sys.exit()
            elif message:
                message = message.encode('utf-8')
                message_header = \
                    f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                server.send(message_header + message)
                sys.stdout.write('<You> ')
                sys.stdout.write(message.decode() + '\n')
                sys.stdout.flush()

