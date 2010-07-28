import pincaster
import unittest

class LayerTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.pincaster = pincaster.Pincaster()
        super(LayerTestCase, self).__init__(*args, **kwargs)
    
    def test_save(self):
        layer = pincaster.Layer('test_layer', self.pincaster)
        layer.save()
    
    def test_delete(self):
        layer = self.pincaster.get_layer('test_layer')
    
    def test_get_all(self):
        layers = self.pincaster.layers
        
        toto = self.pincaster['toto']
        toto.save()
        tata = self.pincaster['tata']
        tata.save()
        
        layers = self.pincaster.layers
