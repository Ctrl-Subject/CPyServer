import socket
import threading

SERVER_IP = "192.168.88.5"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

my_id = None


def receive():
    global my_id

    while True:
        try:
            data = client.recv(1024)

            if not data:
                break

            message = data.decode()

            if message.startswith("ID:"):
                my_id = message[3:]
                print(f"You are Client {my_id}")
            else:
                print(message)

        except:
            break


threading.Thread(target=receive, daemon=True).start()

while True:
    try:
        message = input("> ")
        client.sendall(message.encode())

    except KeyboardInterrupt:
        break

    except:
        break

client.close()