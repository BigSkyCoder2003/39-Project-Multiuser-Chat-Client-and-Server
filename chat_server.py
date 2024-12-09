# Example usage:
#
# python select_server.py 3490

import json
import socket
import select

serverIP = '127.0.0.1'

clients = {}


def broadcast(message, exclude_client = None):
    
    for client in list(clients):
       if client != exclude_client:
          try: 
             send_packet(client, message)
          except Exception as e:
            print(f"Error broadcasting to {clients[client]}: {e}")
            remove_client(client)
             
def send_packet(sock, payload):
    payload_json = json.dumps(payload)
    payload_bytes = payload_json.encode('utf-8')
    payload_length = len(payload_bytes)
    sock.sendall(payload_length.to_bytes(2, byteorder='big')+payload_bytes)


def remove_client(client):
   if client in clients:
      nick = clients.pop(client)
      print(f"*** {nick} has left the chat")
      broadcast({"type": "leave", "nick": nick})
      client.close()

def main():
    """Main server logic."""
    host = "0.0.0.0"
    port = 3490

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(20)
    print(f"*** Server listening on {host}:{port}")

    sockets = [server_socket]

    try:
        while True:
            readable, _, _ = select.select(sockets, [], [])
            
            for s in readable:
                if s == server_socket:
                    client_socket, client_address = server_socket.accept()
                    sockets.append(client_socket)
                    print(f"*** New connection from {client_address}")
                else:
                    try:
                        header = s.recv(2)
                        if not header:
                            remove_client(s)
                            sockets.remove(s)
                            continue
                        
                        payload_length = int.from_bytes(header, byteorder='big')
                        payload = s.recv(payload_length).decode('utf-8')
                        data = json.loads(payload)

                        if data["type"] == "hello":
                            nick = data["nick"]
                            clients[s] = nick
                            print(f"*** {nick} has joined the chat")
                            broadcast({"type": "join", "nick": nick}, )
                        elif data["type"] == "chat":
                            nick = clients[s]
                            print(f"{nick}: {data['message']}")
                            broadcast({"type": "chat", "nick": nick, "message": data["message"]})
                    except Exception as e:
                        print(f"Error handling client {clients.get(s, 'unknown')}: {e}")
                        remove_client(s)
                        sockets.remove(s)
    except KeyboardInterrupt:
        print("*** Server shutting down...")
    finally:
        for s in sockets:
            s.close()

if __name__ == "__main__":
    main()
