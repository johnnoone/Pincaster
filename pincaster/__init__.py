"""
    Pincaster
    ~~~~~~~~~

"""


__version__ = '0.0.1'
__url__ = 'http://github.com/johnnoone/Pincaster'

from exceptions import Http404, RecordUnreachable
from server import Server
from layer import KeySet, Layer, RecordSet
from record import Record
from containers import AtomicInt, ContentStr, UnixDatetime


class Pincaster(object):

    def __init__(self, host='127.0.0.1', port=4269):
        """
        Initialization.
        """
        self.server = Server(host, port)

    def get_layer(self, layer_name):
        """
        Gets or creates layer.

        Parameters:
            layer_name (str): Layer's name
        Returns:
            Layer
        """
        layer = Layer(name=layer_name, server=self)
        return layer

    __getitem__ = get_layer

    @property
    def layers(self):
        """
        Returns all layers.
        """
        response = self.server('/api/1.0/layers/index.json')
        layers = [Layer(server=self, **c) for c in response['layers']]
        return layers

    def ping(self):
        path = '/api/1.0/system/ping.json'
        response = self.server(path)
        return response.get('pong', False)

    def shutdown(self):
        response = self.server('/api/1.0/system/shutdown.json',
                               method='POST',
                               headers={'Connection': 'close'})
        return response

    def rewrite(self):
        path = '/api/1.0/system/rewrite.json'
        response = self.server(path, 'POST')
        return '204' in response
