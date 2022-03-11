from getpass import getpass
from os import environ
from random import randint  
from socket import create_connection, timeout
from threading import Thread
from rich import print
from rich.prompt import Prompt
from rich.table import Table

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team
from champlistloader import champ_to_dict


class TntClient:

    def __init__(self, server: str, buffer_size: int = 2048) -> None:
        self._server = server
        self._buffer_size = buffer_size

    def start(self):  #looks lame because the fstring didnt work with my cool ascii so i used old reliable pile o' print
        print("[red]  _______ ______          __  __   _   _ ______ _________          ______  _____  _  __") #credit: https://www.coolgenerator.com/ascii-text-generator
        print("[yellow] |__   __|  ____|   /\   |  \/  | | \ | |  ____|__   __\ \        / / __ \|  __ \| |/ /") 
        print("[green]    | |  | |__     /  \  | \  / | |  \| | |__     | |   \ \  /\  / / |  | | |__) | ' / ")
        print("[blue]    | |  |  __|   / /\ \ | |\/| | | . ` |  __|    | |    \ \/  \/ /| |  | |  _  /|  <  ")
        print("[magenta]    | |  | |____ / ____ \| |  | | | |\  | |____   | |     \  /\  / | |__| | | \ \| . \ ")
        print("[purple]  __|_|__|______/_/__ _\_\_|_ |_|_|_|_\_|______|  |_|      \/  \/   \____/|_|  \_\_|\_\ ")
        print("[magenta] |__   __|/\   / ____|__   __|_   _/ ____|/ ____| ")
        print("[blue]    | |  /  \ | |       | |    | || |    | (___  ")
        print("[green]    | | / /\ \| |       | |    | || |     \___ \ ")
        print("[yellow]    | |/ ____ \ |____   | |   _| || |____ ____) | ")
        print("[red]    |_/_/    \_\_____|  |_|  |_____\_____|_____/  " )
        print(self.tagline())
        print(" ")
        print(" ")
        client.junction()

    def junction(self):
        while True:
            func=input("What do ye desire?(play, log, quit)")
            if(func=="play"):
                client.gamesetup()
            elif(func=="log"):
                client.stats()
            elif(func=="quit"):
                break
            else:
                print(f"Man idk what {func} means try again.")

    def stats(self):
        self._sock = create_connection((self._server, 5550), timeout=6969)
        setupmsg="s,please"
        self._sock.sendall(setupmsg.encode())
        stats=self._sock.recv(self._buffer_size).decode()
        print(stats)

    def gamesetup(self):
        self._sock = create_connection((self._server, 5550), timeout=6969)
        gamertag=input("Choose your gamertag:")
        setupmsg="g,"+gamertag
        self._sock.sendall(setupmsg.encode())
        while True:
            messaj, pnum = self._sock.recv(self._buffer_size).decode().split(",")
            if(messaj=="rdy2gaming"):
                break
            print(messaj)
        self.gaming(pnum)
    
    def gaming(self, pnum):
        print("game starting:")
        self._sock.sendall("ty".encode())
        self.champs = self._sock.recv(self._buffer_size).decode()
        self.cdict=champ_to_dict(self.champs)
        self.print_available_champs(self.cdict)
        player1 = []
        player2 = []
        if(pnum=="1"):
            self.input_champion('choose your champ', 'red', self.cdict, player1, player2)
        else:
            p1guy, p1gt= self._sock.recv(self._buffer_size).decode().split(',')
            player1.append(p1guy)
            print(p1gt+' chose '+p1guy)
        if(pnum=="2"):
            self.input_champion('choose your champ', 'blue', self.cdict, player2, player1)
        else:
            p2guy, p2gt= self._sock.recv(self._buffer_size).decode().split(',')
            player2.append(p2guy)
            print(p2gt+' chose '+p2guy)
        if(pnum=="1"):
            self.input_champion('choose your champ', 'red', self.cdict, player1, player2)
        else:
            p1guy= self._sock.recv(self._buffer_size).decode()
            player1.append(p1guy)
            print(p1gt+' chose '+p1guy)
        if(pnum=="2"):
            self.input_champion('choose your champ', 'blue', self.cdict, player2, player1)
        else:
            p2guy= self._sock.recv(self._buffer_size).decode()
            player2.append(p2guy)
            print(p2gt+' chose '+p2guy)
        dem_results = self._sock.recv(self._buffer_size).decode()
        print(dem_results)


    def tagline(self):   #a function so i can add more taglines if i have time
        num=randint(1, 6)
        if(num==1):
            return "''We're totally not a clone of DOS Auto Chess''"
        if(num==2):
            return "''It's called tnt because this game blows''"
        if(num==3):
            return "''Like Minecraft if Minecraft was an auto battler''"
        if(num==4):
            return "''tagline''"
        if(num==5):
            return "''One of the games of all time''"
        if(num==6):
            return "''original game do not steal''"

    def print_available_champs(self, champions: dict[Champion]) -> None:
        # Create a table containing available champions
        available_champs = Table(title='Available champions')
        # Add the columns Name, probability of rock, probability of paper and
        # probability of scissors
        available_champs.add_column("Name", style="cyan", no_wrap=True)
        available_champs.add_column("prob(R)", justify="center")
        available_champs.add_column("prob(P)", justify="center")
        available_champs.add_column("prob(S)", justify="center")
        # Populate the table
        for champion in champions.values():
            available_champs.add_row(*champion.str_tuple)
        print(available_champs)

    def input_champion(self, prompt: str,
                   color: str,
                   champions: dict[Champion],
                   player1: list[str],
                   player2: list[str]) -> None:

    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
        while True:
            match Prompt.ask(f'[{color}]{prompt}'):
                case name if name not in champions:
                    print(f'The champion {name} is not available. Try again.')
                case name if name in player1:
                    print(f'{name} is already in your team. Try again.')
                case name if name in player2:
                    print(f'{name} is in the enemy team. Try again.')
                case _:
                    player1.append(name)
                    self._sock.sendall(name.encode())
                    break


if __name__ == "__main__":
    server = environ.get("SERVER", "localhost")
    client = TntClient(server)
    client.start()