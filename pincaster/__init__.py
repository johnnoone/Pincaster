# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright 2010 Xavier Barbosa


__version__ = '0.0.1'
__url__     = 'http://github.com/johnnoone/Pincaster'


from exceptions import *
from server import *
from layer import *
from record import *
from containers import *


class Pincaster(object):
    def __init__(self, host='127.0.0.1', port=4269):
        """
        Initialization.
        """
        
        self.server = server.Server(host, port)
    
    def get_layer(self, layer_name):
        """
        Gets or creates layer.
        
        :keyword layer_name: see :attr:`layer_name`
        
        .. attribute:: layer_name
        
            Layer's name
        
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
    