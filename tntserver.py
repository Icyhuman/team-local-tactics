from asyncio.windows_events import NULL
from contextlib import nullcontext
from os import environ
from socket import create_connection, create_server, timeout
from threading import Lock, Thread


class TntServer:

    def __init__(self, host: str, port: int, backend, buffer_size: int = 2048):
        self._backend=backend
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._heroes = ""
        self._gamer_lock = Lock()
        self._waitingplayer=NULL
        self._wpgt=NULL
        self._sock = create_connection((self._backend, 6969), timeout=6969)
        self._sock.sendall("cl,haha".encode())
        self._heroes = self._sock.recv(self._buffer_size).decode()
        print(self._heroes)
        self.heros=self._heroes.split("\n")
        print(self.heros)

    def turn_on(self):
        self._welcome_sock = create_server(
            (self._host, self._port),
        )
        self._welcome_sock.settimeout(5)
        self._serving = True
        Thread(target=self._accept).start()

    def _accept(self):
        while self._serving:
            try:
                player, _ = self._welcome_sock.accept()
            except timeout:
                pass
            else:
                fun, gtag=player.recv(self._buffer_size).decode().split(",")
                if(fun=="g"):
                    self._gamesetup(player, gtag)
                elif(fun=="s"):
                    Thread(target=self._statfetch, args=(player)).start()

    def _gamesetup(self, player, gtag):
        if(self._waitingplayer==NULL):
            player.sendall("Waiting for p2...".encode())
            self._waitingplayer=player
            self._wpgt=gtag
        else:
            p1=self._waitingplayer
            p1gt=self._wpgt
            self._waitingplayer=NULL
            self._wpgt=NULL
            Thread(target=self._gaming, args=(p1, player, p1gt, gtag)).start()

    def _gaming(self, p1, p2, p1gt, p2gt):
        p1.sendall("rdy2gaming".encode())
        p2.sendall("rdy2gaming".encode())
        p1.sendall(f"sorry {p1gt} no game yet".encode())
        p2.sendall(f"sorry {p2gt} game dont exist yet".encode())

        

if __name__ == "__main__":
    backend = environ.get("SERVER", "localhost")
    host = environ.get("HOST", "localhost")
    server = TntServer(host, 5550, backend)
    server.turn_on()