## new_socket.bind(("212.76.128.141", 2000))

import socket, threading

host = '212.76.128.141'
port = 2000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} GoodBuy!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():  # Подключение нескольких клиентов
    while True:
        client, address = server.accept()
        print("Soedenenia с {}".format(str(address)))
        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print("Nick name {}".format(nickname))
        broadcast("{} Connectin !".format(nickname).encode('utf-8'))
        client.send('Connect to server!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()