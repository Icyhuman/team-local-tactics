from contextlib import nullcontext
from os import environ
from socket import create_server, timeout
from threading import Lock, Thread


class TntServer:

    def __init__(self, host: str, port: int, buffer_size: int = 2048):
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._heroes = {}
        self._gamer_lock = Lock()

    def turn_on(self):
        self._welcome_sock = create_server(
            (self._host, self._port),
        )
        self._welcome_sock.settimeout(5)
        self._serving = True
        Thread(target=self._accept).start()

    def _accept(self):
        nop1=True
        while self._serving and nop1==True:
            try:
                p1, _ = self._welcome_sock.accept()
            except timeout:
                pass
            else:
                p1.sendall("waiting for p2...".encode())
                nop1=False
        while self._serving:
            try:
                p2, _ = self._welcome_sock.accept()
            except timeout:
                pass
            else:
                Thread(target=self._gaming, args=(p1, p2)).start()

    def _gaming(self, p1, p2):
        p2.sendall("Me so sorry game no exist yet".encode())
        p1.sendall("Me so sorry no game yet".encode())

        

if __name__ == "__main__":
    host = environ.get("HOST", "localhost")
    server = TntServer(host, 5550)
    server.turn_on()