# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

serverIP = '127.0.0.1'

def run_server(port):
    
    address = (serverIP, port)
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen()
    
    read_set = []
    client_addresses = {}
    client_buffers = {}

    read_set.append(server)

    while True:
      ready_to_read, _,_ = select.select(read_set, {}, {})
      

      for socket in ready_to_read:
        if socket == server:
            client_socket, client_address = socket.accept()
            read_set.append(client_socket)
            client_addresses[client_socket] = client_address
            print(f'{client_addresses[client_socket]}: connected')
        else:
            
            data = socket.recv(4096)
            if data:
              print(f'{client_addresses[socket]}: {len(data)} bytes: {data}')
            else:
              print(f'{client_addresses[socket]}: disconnected')
              read_set.remove(s)

        

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
