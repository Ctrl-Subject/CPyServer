import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on port {PORT}...")

clients = {}
client_lock = threading.Lock()
next_client_id = 1


def broadcast(sender_id, message):
    with client_lock:
        dead_clients = []

        for client_id, conn in clients.items():
            if client_id != sender_id:
                try:
                    conn.sendall(f"Client {sender_id}: {message}".encode())
                except:
                    dead_clients.append(client_id)

        for client_id in dead_clients:
            clients[client_id].close()
            del clients[client_id]


def handle_client(client_id, conn):
    print(f"Client {client_id} connected.")

    try:
        conn.sendall(f"ID:{client_id}".encode())

        while True:
            data = conn.recv(1024)

            if not data:
                break

            message = data.decode()

            print(f"[Client {client_id}] {message}")

            broadcast(client_id, message)

    except:
        pass

    print(f"Client {client_id} disconnected.")

    with client_lock:
        if client_id in clients:
            clients[client_id].close()
            del clients[client_id]


while True:

    conn, addr = server.accept()

    with client_lock:
        client_id = next_client_id
        next_client_id += 1
        clients[client_id] = conn

    print(f"{addr} assigned Client ID {client_id}")

    threading.Thread(
        target=handle_client,
        args=(client_id, conn),
        daemon=True
    ).start()
