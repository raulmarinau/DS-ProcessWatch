import time
import datetime


class Heartbeat:
    def __init__(self, ip, timestamp=0):
        self.ip = ip
        self.timestamp = timestamp

    def __str__(self):
        utc_timestamp = datetime.datetime.fromtimestamp(self.timestamp)
        return f"Last ping from {self.ip} has timestamp {self.timestamp} ({utc_timestamp})"

    def update_hb(self, timestamp):
        self.timestamp = timestamp

    def check_failure(self):
        if time.time() - self.timestamp > 10 and self.timestamp != 0:
            return True
        return False

    def get_ip(self):
        return self.ip