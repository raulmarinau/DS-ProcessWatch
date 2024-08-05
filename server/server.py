import socket
import datetime
import time
import threading

from common.logger import Logger
from common.heartbeat import Heartbeat


class SimpleServer:
    def __init__(self, connections, host='127.0.0.1', port=1337):
        self._host = host
        self._port = port
        self._open = True
        self._hbs = []
        for ip in connections:
            self._hbs.append(Heartbeat(ip, 0))

    def __str__(self):
        return f"SimpleServer listening on {self._host}:{self._port}"

    def local_address(self):
        return self._host, self._port

    def stop_listening(self):
        self._open = False

    def update_hb(self, ip):
        for hb in self._hbs:
            if ip == hb.get_ip():
                hb.update_hb(time.time())
                return
        Logger.info(f"Err! Unknown ip: {ip}")

    def check_hb(self):
        threading.Timer(5.0, self.check_hb).start()
        for hb in self._hbs:
            if hb.check_failure():
                Logger.warn(f"{hb.get_ip()} failure", requester=type(self).__name__)

    def start_listening(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self._host, self._port))
                s.listen()
                while self._open == True:
                    self.check_hb()
                    conn, addr = s.accept()
                    Logger.info(f"Connection establised with {addr}", requester=type(self).__name__)
                    with conn:
                        data = conn.recv(1024)
                        Logger.info(f"Server received data: {data}", requester=type(self).__name__)
                        self.update_hb(addr[0])
                        if not data:
                            break
                        else:
                            conn.sendall(b"Ack")
        except Exception as e:
            print(e)
