import pincaster
import unittest
from random import randrange

class SearchTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        
        self.pincaster = pincaster.Pincaster()
        self.layer = self.pincaster.get_layer('test_layer')
        super(SearchTestCase, self).__init__(*args, **kwargs)
    
    def setUp(self):
        
        self.layer.save()
    
    def tearDown(self):
        
        self.layer.delete()
    
    def clear_records(self):
        
        self.layer.save()
        self.layer.delete()
        self.layer.save()
    
    def generate_records(self, count=10):
        
        records = {}
        for i in xrange(count):
            key = 'foo:%d:bar:%d:%d' % (i % 2, i % 10, i)
            
            params = {
                'layer': self.layer,
                'key': key,
                'properties': {
                    'name': 'foo:%d:bar:%d' % (i % 2, i % 10),
                    'haha': randrange(1, 100)
                },
            }
            
            record = pincaster.Record(**params)
            record.coords = float(randrange(48400, 48600, 10)) / 1000, float(randrange(1500, 2500, 10)) / 1000
            record.save()
            records[key] = record
        
        return records
        
    
    def test_nearby(self):
        
        self.clear_records()
        
        layer = self.layer
        x = layer.nearby((48.510, 2.240), radius=70000)
        
        assert len(x) == 0
        
        self.generate_records(10)
        x = layer.nearby((48.510, 2.240), radius=70000)
        
        assert len(x) == 10
    
    def test_in_rect(self):
        
        self.clear_records()
        
        layer = self.layer
        x = layer.in_rect((48., 2., 49., 3.))
        
        assert len(x) == 0
        
        records = self.generate_records(20)
        x = layer.in_rect((48.0, 1.0, 49.0, 3.0))
        
        assert len(x) == 20
    
    def test_range_records(self):
        
        self.clear_records()
        layer = self.layer
        
        keys = self.layer.fetch_records('foo-*')
        
        assert len(keys) == 0
        
        records = self.generate_records(20)
        keys = self.layer.fetch_range('foo:*')
        
        assert len(keys) == 20
    
    def test_fetch_keys(self):
        self.clear_records()
        layer = self.layer
        keys = self.layer.fetch_keys('foo:*')
        
        records = self.generate_records(20)
        
        keys = self.layer.fetch_keys('foo:*')
        
        assert len(keys) == 20
    
