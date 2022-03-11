
from os import environ
from socket import create_server, timeout
from threading import Thread
from champlistloader import load_champs_string, load_loserlog, load_some_champs


class tntBackend:

    def __init__(self, host: str, port: int, buffer_size: int = 2048):
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._heroes = load_champs_string()
        print("backend online")

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
                serv, _= self._welcome_sock.accept()
            except timeout:
                pass
            else:
                fun, content=serv.recv(self._buffer_size).decode().split(",")
                if(fun=="cl"):
                    serv.sendall(self._heroes.encode())
                elif(fun=="sf"):
                    self._statfetch(serv)
                elif(fun=="sw"):
                    self._statwrite(content)


    def _statwrite(self, content):
        with open("loserlog.txt", 'a') as f:
            f.write(content+"\n")

    def _statfetch(self, serv):
        log=load_loserlog()
        serv.sendall(log.encode())

if __name__ == "__main__":
    host = environ.get("HOST", "localhost")
    server = tntBackend(host, 6969)
    server.turn_on()