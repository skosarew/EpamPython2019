import socket
from threading import *

HEADER_LENGTH = 10
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = "127.0.0.1"
Port = 1234

server.bind((IP_address, Port))
server.listen(100)

sockets_list = []

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP_address}:{Port}...')


def receive_message(client_socket):
    """Recieve message from client"""
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header,
                'data': client_socket.recv(message_length)}

    except Exception:
        return False


def client_thread(conn, addr):
    while True:
        # Receive message
        message = receive_message(conn)
        if not message:
            """message may have no content if the connection 
            is broken, in this case we remove the connection"""

            print('Closed connection from: {}'.format(addr[0]))
            sockets_list.remove(conn)
            print(str(addr[0]) + ':' + str(addr[1]) + ' disconnected')
            conn.close()
            break

        user = clients[conn]
        print(f'Received message from {user["data"].decode("utf-8")}: '
              f'{message["data"].decode("utf-8")}')

        # Send message to specific client
        if message['data'].decode("utf-8").startswith('@'):
            send_specific_client(message, user)

        # Show list of members
        elif message['data'].decode("utf-8") == 'members':
            for socket, item in clients.items():
                conn.send(user['header'] + user['data'] + item['header'] +
                          item['data'])
        # Send message to all members
        elif message is not False:
            broadcast(message, conn, user)


def send_specific_client(message, user):
    """Sends message to specific client"""
    data = message['data'].decode().split()
    specific_client_name = data[0][1:].encode('utf-8')
    data_to_specific_client = data[1:]
    message['data'] = ' '.join(data_to_specific_client).encode('utf-8')
    message_length = len(message['data'])
    message['header'] = (str(message_length) + ' ' * (HEADER_LENGTH - len(str(
        message_length)))).encode('utf-8')
    for socket, client in clients.items():
        if client['data'] == specific_client_name:
            socket.send(
                user['header'] + user['data'] + message['header'] +
                message['data'])


def broadcast(message, connection, user):
    for clients in sockets_list:
        if clients != connection:
            try:
                clients.send(
                    user['header'] + user['data'] + message['header'] +
                    message['data'])
            except Exception as err:
                print('err', err)
                clients.close()

                # if the link is broken, we remove the client
                remove(clients)


def remove(connection):
    if connection in sockets_list:
        sockets_list.remove(connection)


while True:
    conn, addr = server.accept()
    user = receive_message(conn)

    print(f"New connection from {addr[0]}:{addr[1]}, username: "
          f"{user['data'].decode('utf-8')}")

    sockets_list.append(conn)
    clients[conn] = user

    # creates and individual thread for every user that connects
    server_thread = Thread(target=client_thread, args=(conn, addr))
    server_thread.daemon = True
    server_thread.start()
