import socket
import selectors


class SocketHandler:
    def __init__(self, host: str, port: int, on_new_client=None, on_message=None):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.selector = selectors.DefaultSelector()
        self.on_new_client = on_new_client
        self.on_message = on_message

    def start_server(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ, self._accept_connection)
        print(f"Server is active on {self.host}:{self.port}")

        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def _accept_connection(self, sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(False)
        if self.on_new_client:
            self.on_new_client(conn, addr)
        self.selector.register(conn, selectors.EVENT_READ, self._read_message)

    def _read_message(self, conn, mask):
        data = conn.recv(1024)
        if data:
            if self.on_message:
                self.on_message(conn, data)
        else:
            print(f"Closing connection to {conn.getpeername()}")
            self.selector.unregister(conn)
            conn.close()

    def send_data(self, conn, message: str):
        conn.send(message.encode())


# Handlers for client connections and messages
def handle_new_client(conn, addr):
    print(f"New connection from {addr}")


def handle_message(conn, data):
    print(f"Received data from {conn.getpeername()}: {data.decode()}")
    response = "Message received, THX"
    socket_server.send_data(conn, response)


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432

    socket_server = SocketHandler(HOST, PORT, handle_new_client, handle_message)
    socket_server.start_server()
