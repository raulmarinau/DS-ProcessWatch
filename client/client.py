import socket
import time
import random

from common.logger import Logger


class SimpleClient:
    def __init__(self, host='127.0.0.1', port=1337):
        self._host = host
        self._port = port

    def __str__(self):
        return f"SimpleClient sending to {self._host}:{self._port}"

    def new_connection(self, host, port):
        self._host = host
        self._port = port

    def send(self):
        try:
            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self._host, self._port))
                    s.sendall(b'Ping')
                    data = s.recv(1024)
                    Logger.info(f'Received {repr(data)}', requester=type(self).__name__)
                time.sleep(5)
        except Exception as e:
            print(e)


class MultiConnClient(SimpleClient):
    def __init__(self, connections):
        self._connections = connections
        self._index = 0
        self._port = 1337

    def update_index(self):
        self._index = self._index + 1
        if self._index == len(self._connections):
            self._index = 0

    def send(self):
        try:
            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    Logger.info(f"Connecting to {self._connections[self._index]}:{self._port}")
                    s.connect((self._connections[self._index], self._port))
                    s.sendall(b'Ping')
                    data = s.recv(1024)
                    Logger.info(f'Received {repr(data)}', requester=type(self).__name__)
                self.update_index()
                time.sleep(2)
        except Exception as e:
            print(e)
