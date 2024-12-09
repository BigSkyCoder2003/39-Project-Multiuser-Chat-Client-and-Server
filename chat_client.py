import sys
import socket
import json
import threading
from chatui import init_windows, read_command, print_message, end_windows


def usage():
    print("usage: chat_client.py user’s_nickname, server_address, server_port", file=sys.stderr)


def send_messages(sock, nick, stop_event):
    while True:
        user_input = read_command(f'{nick}> ')
        if user_input.startswith('/q'):
            print_message("*** Exiting chat. Goodbye!")
            stop_event.set()
            sock.close()
            break
        else:
            message_payload = {
                "type": "chat",
                "message": user_input
            }
            send_packet(sock, message_payload)


def recieve_messages(sock, stop_event):
    while not stop_event.is_set(): 
        header = sock.recv(2)
        payload_length = int.from_bytes(header, byteorder="big")
        payload = sock.recv(payload_length).decode('utf-8')
        data = json.loads(payload)

        if data["type"] == "chat":
            print_message(f"{data['nick']}: {data['message']}")
        elif data["type"] == "join":
            print_message(f"{data['nick']}: has joined the chat")
        elif data["type"] == "leave":
            print_message(f"{data['nick']}: has left the chat")



def send_packet(sock, payload):
    payload_json = json.dumps(payload)
    payload_bytes = payload_json.encode('utf-8')
    payload_length = len(payload_bytes)
    sock.sendall(payload_length.to_bytes(2, byteorder = 'big') + payload_bytes)


def main(argv):
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)
    init_windows()
    
    nick, server, port = sys.argv[1], sys.argv[2], int(sys.argv[3])

    sock = socket.socket()
    sock.connect((server, port))
    print(f"*** Connected to server at {server}:{port}")

    hello_payload = {
        "type": "hello",
        "nick": nick
    }
    send_packet(sock, hello_payload)

    stop_event = threading.Event()
    send_thread = threading.Thread(target=send_messages, args=(sock, nick, stop_event))
    recieve_thread = threading.Thread(target=recieve_messages, args=(sock, stop_event))
    recieve_thread.daemon = True
    send_thread.start()
    recieve_thread.start()

    send_thread.join()

    end_windows()
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
