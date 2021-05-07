import socket
import sys

class TDServer:
    def __init__(self, ip_addr, port, DEBUG=False):
        self.testing = DEBUG
        self.ip = ip_addr
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CloseUP = False
        self.buffer = ""
        self.server_address = (self.ip,self.port)
        self.sock.bind(self.server_address)
        self.sock.listen(1)

    def CheckConnection(self):
        print("entering checkconnection")
        connection, client_address = self.sock.accept()
        if self.testing is True: print(f'enter try')
        data = connection.recv(16)
        if data:
            if self.testing is True: print(f'data: {data}')
            #self.buffer += data
        else:
            if self.testing is True: print(f'buffer:{self.buffer}')