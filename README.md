# Final Project: Multiuser Chat Server and Client 
# Daniel Lounsbury
# Brian Hall
# CS372

## Chat Client Documentation

### `usage() -> None`
Displays how to run the script with correct arguments.

### `send_messages(sock, nick, stop_event) -> None`
Waits for the user to type a message and sends it to the server. Stops if "/q" is typed.

### `receive_messages(sock, stop_event) -> None`
Waits for and shows messages from the server.

### `send_packet(sock, payload) -> None`
Sends a message (in JSON format) to the server.

### `main(argv) -> None`
Starts the chat client, connects to the server, and runs the message send and receive functions.

## Chat Server Documentation

### `broadcast(message, exclude_client=None) -> None`
Sends a message to all connected clients except the specified one.

### `send_packet(sock, payload) -> None`
Sends a message to the client in JSON format.

### `remove_client(client) -> None`
Removes a client from the server and broadcasts their departure.

### `main() -> None`
Sets up the server, listens for connections, and handles messages from clients.