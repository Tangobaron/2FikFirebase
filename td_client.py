import socket
import sys

class TDClient:
    def __init__(self, ip_addr, port, DEBUG=False):
        self.families = self.get_constants('AF_')
        self.testing = DEBUG
        self.ip = ip_addr
        self.port = port
        self.types = self.get_constants('SOCK_')
        self.protocols = self.get_constants('IPPROTO_')
        self.sock = socket.create_connection((ip_addr, port))
        self.buffer = ""
    #basic setup for tcp connection source https://pymotw.com/2/socket/tcp.html
    def get_constants(self, prefix):
        """Create a dictionary mapping socket module constants to their names."""
        return dict( (getattr(socket, n), n)
            for n in dir(socket)
                if n.startswith(prefix)
                )
	
    def composeMessage(self, name, data):
        msg = ''
        i = 0
        for subject in data:
            msg += str(name[i]) + "::"
            msg += str(subject) + ";; "
            i += 1
        msg += "\r\n"
        return msg

    def AddToBuffer(self, name, data):
        self.buffer += self.composeMessage(name,data)

    def SendMessage(self):
        #message = str.encode(self.composeMessage(name,data))
        message = str.encode(self.buffer)
        #print(message)
        self.sock.sendall(message)
        self.buffer = ""
        if self.testing == True: print(f'message sent {message} at server: {self.ip}:{self.port}')