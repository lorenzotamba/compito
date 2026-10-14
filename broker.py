import socket
import threading

subscribers = []
subscribers_lock = threading.Lock()

class broker(threading.Thread):
    def __init__(self,c,addr):
        super().__init__()
        self.c = c
        self.addr = addr

    def run(self):
        self.ricevi_invia(self.c)
        with subscribers_lock:
            if self.c in subscribers:
                subscribers.remove(self.c)
        self.c.close()

    def readLine(self, sk):
        data = b''
        while b'\n' not in data:
            packet = sk.recv(1024)
            if not packet:
                return b''
            data += packet
        line, _ = data.split(b'\n', 1)
        return line.strip()

    def ricevi_invia(self,sock):
        while True:
            request = self.readLine(sock).decode()

            if not request:
                break

            if request.lower() == "sub:topic":

                with subscribers_lock:
                    if sock not in subscribers:
                        subscribers.append(sock)

                response = "subscriber" + "\n"
                sock.sendall(response.encode())
                print("messaggio inviato al subscriber")

            elif request.startswith("pub:topic:") or request == "MESSAGGIO":
                print(f"Inoltro messaggio ai subscriber: {request}")
                msg_to_send = (request + "\n").encode()

                with subscribers_lock:
                    for sub_sock in subscribers[:]:
                        try:
                            sub_sock.sendall(msg_to_send)
                        except Exception:
                            subscribers.remove(sub_sock)




def main():
    host = ''
    port = 12346
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print('Server started.')
    while True:
        c, addr = s.accept()
        print('client connected ip:<' + str(addr) + '>')
        t = threading.Thread(target=broker, args=(c, addr))
        t.start()

if __name__ == "__main__":
    main()