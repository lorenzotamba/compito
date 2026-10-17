import socket

def Main():
    host = '192.168.14.39'
    port = 12346
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    message ="sub:topic"
    sock.send((message + '\n').encode())
    while True:
        data = sock.recv(1024)
        print(data.decode())

if __name__ == '__main__':
    Main()