import socket
import threading

HOST = '192.168.43.237'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def brodcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            brodcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"le client {str(address)} est connceté")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"-> {nickname}")
        brodcast(f"{nickname} est conncter au server\n".encode('utf-8'))
        client.send("connecter au server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("demarage du serveur")
receive()