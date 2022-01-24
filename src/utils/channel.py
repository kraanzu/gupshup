from struct import pack, unpack
from socket import socket
from pickle import dumps, loads
from sys import getsizeof as sizeof


class Channel:
    """
    A Message class that sends and recieves data
    by pre-calculating the size of the data to be recieved
    so that there are no overloads or packet losses
    """

    def __init__(self, conn: socket):
        self.conn = conn

    def send(self, data):
        """
        First sends the size of the data using struct's pack()
        then the data itself
        """

        data_encoded = dumps(data)
        bufsize = pack("!i", sizeof(data_encoded))
        self.conn.sendall(bufsize)
        self.conn.sendall(data_encoded)

    def recv(self):
        """
        A recv_all type method that
        ensures that there is no data loss
        """

        bufsize = unpack("!i", self.conn.recv(37))[
            0
        ]  # 37 seems to be the size of a packed `int`
        data = loads(self.conn.recv(bufsize))
        return data
