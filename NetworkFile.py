import socket
import pickle



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "213.226.119.174"  # server2
        # self.server = "45.12.253.236"  # server1
        self.server = "192.168.202.28"  # local
        self.port = 8001
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getPlayer(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.receive_data())
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
            return pickle.loads(self.receive_data())
        except Exception as e:
            print(e)

    def receive_data(self):
        buffer_size = 4096  # Choose an appropriate buffer size
        received_data = b""
        while True:
            data = self.client.recv(buffer_size)
            if not data:
                break
            received_data += data
            if len(data) < buffer_size:
                break
        return received_data