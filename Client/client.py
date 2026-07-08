import socket
import threading

SERVER_IP = "10.57.14.71"

HOST = SERVER_IP
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected!")


def receive():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            print(f"\nPeer: {data.decode()}")
        except:
            break


threading.Thread(target=receive, daemon=True).start()

while True:
    try:
        msg = input("You: ")
        client.sendall(msg.encode())
    except KeyboardInterrupt:
        break
    except:
        break

client.close()