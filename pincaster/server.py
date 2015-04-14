__all__ = ['Server']

import json
import socket
import urllib

from exceptions import Http404
from containers import AtomicInt

json_hook = lambda x: dict([(str(k), v) for k, v in x.iteritems()])


def json_hook(dct):
    """
    Cast socalled int() into AtomicInt() and keys in str().
    """

    out = {}
    for k, v in dct.iteritems():
        if isinstance(v, (unicode, str, int)):
            try:
                v = AtomicInt(v)
            except ValueError:
                pass
        out[str(k)] = v
    return out


class Server(object):

    def __init__(self, host='127.0.0.1', port=4269):
        self._host = host
        self._port = port

    def __call__(self, uri, method=None, data=None, headers=None):
        try:
            return self._command(uri, method, data, headers)
        except:
            self.sock(True)
            return self._command(uri, method, data, headers)

    command = __call__

    def sock(self, force=False):
        if force or not getattr(self, '_sock', False):
            self.connect()
        return self._sock

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.connect((self._host, self._port))
        self._sock = sock

    def _command(self, uri, method=None, data=None, headers=None):
        method = method or 'GET'
        data = data or {}
        query = urllib.urlencode(data)

        if method == 'GET' and query:
            sep = '?' in uri and '&' or '?'
            uri = '%s%s%s' % (uri, sep, query)
            query = ''

        sock = self.sock()
        sock.send('%s %s HTTP/1.1\n' % (method, uri))

        h = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'python/socket',
            'Connection': 'Keep-Alive'
        }
        h.update(headers or {})

        for k, v in h.iteritems():
            sock.send("%s: %s\n" % (k, v))

        if query:
            sock.send("Content-Length: %d""\n\n" % len(query))
            sock.send(query)
        else:
            sock.send("Content-Length: 0\n\n")

        buff = sock.recv(20)
        while '\r\n\r\n' not in buff:
            buff = buff + sock.recv(20)

        headers, body = buff.split('\r\n\r\n', 2)
        headers = headers.splitlines()
        statusline = headers.pop(0)
        headers = dict([tuple(i.split(': ', 2)) for i in headers])

        if 'HTTP/1.1 404 Not Found' in statusline:
            raise Http404

        if 'Content-Length' in headers:
            body = body + sock.recv(int(headers['Content-Length']) - len(body))
        else:
            # Pas le choix, on doit boucler
            buf = []
            while True:
                s = sock.recv(20)
                if s == '':
                    break
                buf.append(s)
            body += ''.join(buf)

        # if h['Connection'] == 'close':
        #     sock.close()

        # le serveur est un peu nazi,
        # on va cacher les erreurs d'interpretations
        if method == 'POST' and body == '':
            return True

        if 'Content-Type' in headers and 'json' in headers['Content-Type']:
            return json.loads(body, object_hook=json_hook)

        # Casse bonbon, on retourne la reponse brute
        return body

    def __str__(self):
        return '%s:%s' % (self._host, self._port)
