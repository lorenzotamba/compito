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
        while (b'\n' not in data):
            data += sk.recv(1024)
        return data.strip()

    def ricevi_invia(self,sock):
        while True:
            request = self.readLine(sock).decode()

            if request.startswith("sub"):
                lista=request.split(":")
                topic=lista[1]

                with subscribers_lock:
                    if (sock,topic) not in subscribers:
                        subscribers.append((sock, topic))

                response = "subscriber" + "\n"
                sock.sendall(response.encode())
                print("messaggio inviato al subscriber")

            elif request.startswith("pub"):
                request=request.split(":")
                topic=request[1]
                message=request[2]
                msg_to_send = (message + "\n").encode()

                with subscribers_lock:
                    for sub_tuple in subscribers[:]:
                        sub_sock, sub_topic = sub_tuple
                        if sub_topic==topic:
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
        #t = threading.Thread(target=broker, args=(c, addr))
        t = broker(c, addr)
        t.start()

if __name__ == "__main__":
    main()