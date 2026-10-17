#python3 ClientPubblisher.py pub:meteo:messaggio

import socket
import sys

def Main():
    host = '192.168.14.39'
    port = 12346
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    message = sys.argv[1]
    sock.send((message + '\n').encode())
    sock.close()

if __name__ == '__main__':
    Main()