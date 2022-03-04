from getpass import getpass
from os import environ  
from socket import create_connection, timeout
from threading import Thread


class TntClient:

    def __init__(self, server: str, buffer_size: int = 2048) -> None:
        self._server = server
        self._buffer_size = buffer_size

    def start(self):  #looks lame because the fstring didnt work with my cool ascii so i used old reliable pile o' print
        print("  _______ ______          __  __   _   _ ______ _________          ______  _____  _  __") #credit: https://www.coolgenerator.com/ascii-text-generator
        print(" |__   __|  ____|   /\   |  \/  | | \ | |  ____|__   __\ \        / / __ \|  __ \| |/ /") 
        print("    | |  | |__     /  \  | \  / | |  \| | |__     | |   \ \  /\  / / |  | | |__) | ' / ")
        print("    | |  |  __|   / /\ \ | |\/| | | . ` |  __|    | |    \ \/  \/ /| |  | |  _  /|  <  ")
        print("    | |  | |____ / ____ \| |  | | | |\  | |____   | |     \  /\  / | |__| | | \ \| . \ ")
        print("  __|_|__|______/_/__ _\_\_|_ |_|_|_|_\_|______|  |_|      \/  \/   \____/|_|  \_\_|\_\ ")
        print(" |__   __|/\   / ____|__   __|_   _/ ____|/ ____| ")
        print("    | |  /  \ | |       | |    | || |    | (___  ")
        print("    | | / /\ \| |       | |    | || |     \___ \ ")
        print("    | |/ ____ \ |____   | |   _| || |____ ____) | ")
        print("    |_/_/    \_\_____|  |_|  |_____\_____|_____/  " )
        print("''It's called tnt because this game blows''")
        print(" ")
        print(" ")
        client.gaming()


    def gaming(self):
        self._sock = create_connection((self._server, 5550), timeout=69)
        while True:
            messaj = self._sock.recv(self._buffer_size).decode()
            print(messaj)

if __name__ == "__main__":
    server = environ.get("SERVER", "localhost")
    client = TntClient(server)
    client.start()