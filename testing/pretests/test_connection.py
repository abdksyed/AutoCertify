# test_connection.py

from functools import wraps
import socket

_REMOTE_SERVER = "one.one.one.one"


def connection_test(fn: callable):
    '''
    A Decorators, which decorates fn by running the function only if there is 
    an active Internet connection or else raise an Exception.
    
    Arguments:
        fn - Callabl function which is to be decorated.
    Returns:
        Return of the input function with it's args and kwargs.
    '''
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            # see if we can resolve the host name
            # tells us if there is a DNS listening
            host = socket.gethostbyname(_REMOTE_SERVER)

            # connect to the host
            # tells us if the host is actually reachable
            s = socket.create_connection((host, 80), 2)
            s.close()

            return fn(*args, **kwargs)

        except socket.gaierror:
            raise Exception('NO INTERNET CONNECTION FOUND. Please connect to internet before proceeding.')

    return inner