# client.py
import socket
import threading
import sys

HOST = '127.0.0.1'   # server IP (use server machine IP if not local)
PORT = 12345

nick = input("Enter your nickname: ").strip()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def receive():
    """Background thread to receive messages from server and print them."""
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                print("Disconnected from server.")
                break
            # server might ask for NICK?
            if msg == b"NICK?":
                sock.send(nick.encode('utf-8'))
                continue
            print(msg.decode('utf-8'))
        except:
            print("Error receiving data.")
            break
    sock.close()
    sys.exit()

def write():
    """Send user-typed messages to the server."""
    while True:
        text = input()
        if text.lower() == '/quit':
            sock.close()
            print("You left the chat.")
            sys.exit()
        try:
            message = f"{nick}: {text}"
            sock.send(message.encode('utf-8'))
        except:
            print("Failed to send. Connection closed.")
            break

# start receiver thread
threading.Thread(target=receive, daemon=True).start()
# start writing loop (main thread)
write()
