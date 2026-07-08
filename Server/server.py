import socket
import threading

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Listening on port {PORT}...")

conn, addr = server.accept()
print(f"Connected by {addr}")


def receive():
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"\nPeer: {data.decode()}")
        except:
            break


threading.Thread(target=receive, daemon=True).start()

while True:
    try:
        msg = input("You: ")
        conn.sendall(msg.encode())
    except KeyboardInterrupt:
        break
    except:
        break

conn.close()
server.close()
