import socket
import threading
import os

# Serverio nustatymai internetui
# Render platforma automatiškai priskiria prievadą (Port) per aplinkos kintamąjį
PORT = int(os.environ.get("PORT", 55555))
HOST = '0.0.0.0'  # Klausomasi visų ateinančių jungčių

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

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
            broadcast(f'[SERVERIS] {nickname} paliko pokalbį.\n'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    print(f"[SERVERIS] Paleistas ir klausosi prievado {PORT}...")
    while True:
        client, address = server.accept()
        print(f"[SERVERIS] Prisijungė naujas įrenginio adresas: {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"[SERVERIS] Vartotojo slapyvardis: {nickname}")
        broadcast(f"[SERVERIS] {nickname} prisijungė prie pokalbių kambario!\n".encode('utf-8'))
        client.send('[SERVERIS] Sėkmingai prisijungei prie serverio!\n'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
