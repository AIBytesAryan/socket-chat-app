# server.py
import socket
import threading

HOST = '0.0.0.0'   # listen on all network interfaces
PORT = 12345       # port to listen on

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server listening on {HOST}:{PORT}")

clients = []        # list of client sockets
nicknames = {}      # map client socket -> nickname

def broadcast(message, _except=None):
    """Send message to all connected clients except _except (if given)."""
    for c in clients:
        if c is not _except:
            try:
                c.send(message)
            except:
                # if send fails, remove client
                try:
                    clients.remove(c)
                except:
                    pass

def handle_client(client_sock):
    """Receive messages from this client and broadcast them."""
    while True:
        try:
            msg = client_sock.recv(1024)  # receive up to 1024 bytes
            if not msg:
                break  # client disconnected
            broadcast(msg, _except=client_sock)
        except:
            break
    # cleanup when client disconnects
    print(f"Client {nicknames.get(client_sock, '')} disconnected")
    try:
        clients.remove(client_sock)
        del nicknames[client_sock]
    except:
        pass
    client_sock.close()

def accept_clients():
    """Accept new clients and start a handler thread for each."""
    while True:
        client_sock, addr = server.accept()
        print("Connected by", addr)
        client_sock.send(b"NICK?")   # ask client for a nickname
        nick = client_sock.recv(1024).decode('utf-8').strip()
        nicknames[client_sock] = nick
        clients.append(client_sock)
        print(f"Nickname: {nick}")
        # announce join to others
        broadcast(f"*** {nick} joined the chat ***".encode('utf-8'), _except=client_sock)
        client_sock.send(b"*** Connected to server ***")
        # start thread to handle this client
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

accept_clients()
