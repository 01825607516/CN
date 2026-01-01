import socket
import threading

host = '127.0.0.1'
port = 5555

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
            if message.decode().startswith("/nickname "):
                index = clients.index(client)
                old_nick = nicknames[index]
                new_nick = message.decode().split(" ", 1)[1]
                nicknames[index] = new_nick
                broadcast(f"[Server] {old_nick} changed nickname to {new_nick}".encode('utf-8'))
                send_online_users()
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            disconnected_nick = nicknames[index]
            clients.remove(client)
            nicknames.pop(index)
            broadcast(f"[Server] {disconnected_nick} left the chat.".encode('utf-8'))
            send_online_users()
            break

def send_online_users():
    users = "/online " + ",".join(nicknames)
    broadcast(users.encode('utf-8'))

def receive():
    print("[Server Running] Waiting for connections...")
    while True:
        client, address = server.accept()
        print(f"[Connection] {address} connected.")
        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f"[Nickname] {nickname}")
        broadcast(f"[Server] {nickname} joined the chat.".encode('utf-8'))
        send_online_users()
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
