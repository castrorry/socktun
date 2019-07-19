import socket
import ssl
import threading
from socktun import Config, Handler

class Proxy:
    def __init__(self):
        self.host = Config.middle_host
        self.ports = Config.middle_ports
        self.event = threading.Event()

    def start(self):
        for port in self.ports:
            s = threading.Thread(target=self.listen, args=(port,))
            s.setDaemon(True)
            s.start()

        self.event.wait()
    
    def listen(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, port))
        sock.listen(5)
        try:
            while True:
                try:
                    io = Handler(sock.accept())
                    io.start()
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            sock.close()
            sock.shutdown(socket.SHUT_RDWR)
            exit(1)
        finally:
            return

