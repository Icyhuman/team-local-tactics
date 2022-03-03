from getpass import getpass
from os import environ  
from queue import Queue
from socket import create_connection, timeout
from threading import Thread


class TntClient:

    def __init__(self, server: str, buffer_size: int = 2048) -> None:
        self._server = server
        self._buffer_size = buffer_size
        self._messages = Queue()
    def start(self):
        self._sock = create_connection((self._server, 5550), timeout=69)
        while True:
            messaj = self._sock.recv(self._buffer_size).decode()
            print(messaj)

if __name__ == "__main__":
    server = environ.get("SERVER", "localhost")
    client = TntClient(server)
    client.start()