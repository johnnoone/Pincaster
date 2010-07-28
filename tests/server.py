import pincaster
import unittest

class ServerTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.pincaster = pincaster.Pincaster()
        self.layer = self.pincaster.get_layer('test_layer')
        super(ServerTestCase, self).__init__(*args, **kwargs)
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
    def test_ping(self):
        
        assert self.pincaster.ping() == 'pong'
    
    def test_rewrite(self):
        
        assert self.pincaster.rewrite() == True
    
    # def test_shutdown(self):
    #     assert self.pincaster.shutdown() == True
    
