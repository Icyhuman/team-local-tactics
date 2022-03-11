from asyncio.windows_events import NULL
from contextlib import nullcontext
from os import environ
from socket import create_connection, create_server, timeout
from threading import Lock, Thread
from rich.table import Table

from champlistloader import champ_to_dict
from core import Champion, Match, Shape, Team


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
        print("servers be like lmao im on rn")

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
            player.sendall("Waiting for p2...,hehe".encode())
            self._waitingplayer=player
            self._wpgt=gtag
        else:
            p1=self._waitingplayer
            p1gt=self._wpgt
            self._waitingplayer=NULL
            self._wpgt=NULL
            Thread(target=self._gaming, args=(p1, player, p1gt, gtag)).start()

    def _gaming(self, p1, p2, p1gt, p2gt):
        p1.sendall("rdy2gaming,1".encode())
        p2.sendall("rdy2gaming,2".encode())
        self._sock.sendall("cl,haha".encode())
        self._heroes = self._sock.recv(self._buffer_size).decode()
        print(self._heroes)
        self._herodict=champ_to_dict(self._heroes)
        p1.recv(self._buffer_size)
        p2.recv(self._buffer_size)
        p1.sendall(self._heroes.encode())
        p2.sendall(self._heroes.encode())
        player1 = []
        player2 = []
        p1champ=p1.recv(self._buffer_size).decode()
        player1.append(p1champ)
        p2.sendall(p1champ.encode())
        p2champ=p2.recv(self._buffer_size).decode()
        player2.append(p2champ)
        p1.sendall(p2champ.encode())
        p1champ=p1.recv(self._buffer_size).decode()
        player1.append(p1champ)
        p2.sendall(p1champ.encode())
        p2champ=p2.recv(self._buffer_size).decode()
        player2.append(p2champ)
        p1.sendall(p2champ.encode())
        match = Match(
        Team([self._herodict[name] for name in player1]),
        Team([self._herodict[name] for name in player2])
        )
        match.play()

        # Handle the summary
        self.handle_match_summary(match, p1, p2, p1gt, p2gt)

    def handle_match_summary(self, match: Match, p1, p2, p1gt, p2gt) -> None:
        results=""
        MOVE = {
            Shape.ROCK: 'R',
            Shape.PAPER: 'P',
            Shape.SCISSORS: 'S'
        }

        # For each round print a table with the results
        for index, round in enumerate(match.rounds):

            # Create a table containing the results of the round
            results+=f'Round {index+1}\n'
            # Populate the table
            for key in round:
                red, blue = key.split(', ')
                results+=f'{red} {MOVE[round[key].red]}, '
                results+=f'{blue} {MOVE[round[key].blue]}\n'
            print('\n')

        # Print the score
        red_score, blue_score = match.score
        results+=f'Red: {red_score}\n'
        results+=f'Blue: {blue_score}'

        # Print the winner
        if red_score > blue_score:
            results+='\n[red]Red victory! smile emoji'
            logentry=f"sw,{p2gt} lost to {p1gt} cause they suck"
        elif red_score < blue_score:
            results+='\n[blue]Blue victory! smile emoji'
            logentry=f"sw,{p1gt} lost to {p2gt} lmao"
        else:
            results+='\nDraw neutral emoji'
            logentry=f"sw,{p2gt} and {p1gt} both lost man they are bad"
        p1.sendall(results.encode())
        p2.sendall(results.encode())
        self._sock = create_connection((self._backend, 6969), timeout=6969)
        self._sock.sendall(logentry.encode())

        

if __name__ == "__main__":
    backend = environ.get("SERVER", "localhost")
    host = environ.get("HOST", "localhost")
    server = TntServer(host, 5550, backend)
    server.turn_on()