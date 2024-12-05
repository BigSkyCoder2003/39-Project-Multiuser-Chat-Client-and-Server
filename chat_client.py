import sys
import socket
from chatui import init_windows, read_command, print_message, end_windows


def usage():
    print("usage: select_client.py user’s_nickname, server_address, server_port", file=sys.stderr)

def main(argv):
    try:
        prefix = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()  
        return 1

    # Make the client socket and connect
    s = socket.socket()
    s.connect((host, port))

    # Loop forever sending data at random time intervals
    while True:
        string_to_send = f"{prefix}: {random_string()}"
        string_bytes = string_to_send.encode()
        s.send(string_bytes)

        delay_random_time()

if __name__ == "__main__":
    sys.exit(main(sys.argv))