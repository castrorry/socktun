import select
import socket
import threading
from socktun import Config

class Handler(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.client, self.client_addr = sock
        self.start_package = bytes()
        self.client.settimeout(30)
        self.destination = self.setDestination()
        self.setDaemon(True)

    def run(self):
        try:
            self.io()
        except:
            return
        finally:
            return

    def setDestination(self):
        tunType = None
        print('Nova conexão de {}'.format(self.client_addr))
        while tunType != 'SSL/TLS' and tunType != 'SSH':
            tunType = self.unmarshal()
        
        if tunType == 'SSL/TLS':
            return socket.create_connection(
                (Config.dest_host, Config.dest_port["tls"])
            )
        elif tunType == 'SSH':
            return socket.create_connection(
                (Config.dest_host, Config.dest_port["tcp"])
            )
        else:
            return None

    def unmarshal(self):
        self.start_package = self.client.recv(5)
        if self.start_package.startswith(b'\x16\x03\x01'):
            return 'SSL/TLS'
        elif self.start_package.startswith(b'SSH-'):
            return 'SSH'
        else:
            self.start_package += self.client.recv(2*1024)
            if self.payload_handler() == 'SSH':
                return 'SSH'
            else:
                return 'HTTP'
    
    def payload_handler(self):
        http_req = self.start_package.split(b'\r\n')
        if http_req[len(http_req)-2].startswith(b'SSH-'):
            return 'SSH'
        else:
            self.client.send(b'HTTP/1.1 200 OK\r\n\r\n')
            self.client.settimeout(10)
            return 'HTTP'
    
    def io(self):
        i = self.client
        o = self.destination
        starting = True
        while True:
            try:
                r, _, _ = select.select([o, i], [], [], 300)
                if not r:
                    break
                if o in r:
                    data = o.recv(1024*32)
                    if len(data) == 0:
                        break
                    i.send(data)
                if i in r:
                    data = i.recv(1024*16)
                    if len(data) == 0:
                        break
                    if starting:
                        starting = False
                        o.send(self.start_package+data)
                    else:
                        o.send(data)
            except socket.timeout:
                break
        try:
            o.shutdown(socket.SHUT_RDWR)
            o.close()
        except:
            pass
        i.shutdown(socket.SHUT_RDWR)
        i.close()
        print('Client {} disconnected'.format(self.client_addr))
        return