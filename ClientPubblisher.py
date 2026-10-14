import socket
import time


def Main():
    host = '192.168.14.40'
    port = 12346
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    message ="pub:topic:message"
    sock.send((message + '\n').encode())
    while True:
        message = "MESSAGGIO"
        sock.send((message + '\n').encode())
        time.sleep(3)

if __name__ == '__main__':
    Main()