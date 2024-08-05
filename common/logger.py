'''Logging utility'''
import datetime

class Logger:
    ''' Logging utils class'''

    @staticmethod
    def info(message, requester='sys'):
        '''info debug lvl'''
        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{curr_time}] > {requester} > INFO > {message}")

    @staticmethod
    def warn(message, requester='sys'):
        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{curr_time}] > {requester} > WARN > {message}")
