import pincaster
import unittest

class RecordTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        
        self.pincaster = pincaster.Pincaster()
        self.layer = self.pincaster.get_layer('test_layer')
        super(RecordTestCase, self).__init__(*args, **kwargs)
    
    def setUp(self):
        
        self.layer.save()
    
    def tearDown(self):
        
        self.layer.delete()
    
    def test_content_plain(self):
        
        toto = self.layer['toto']
        toto.content = ('foo-bar\nbaz', 'text/plain')
        
        assert toto.content == 'foo-bar\nbaz'
        assert toto.content.type == 'text/plain'
        assert toto.content.public_uri == '/public/test_layer/toto'
        
        toto.save()
        fetched = self.layer.pincaster.server(toto.content.public_uri)
        
        assert toto.content == fetched
        
    
    def test_content_html(self):
        
        toto = self.layer['toto']
        
        class S(str): pass
                
        c = S('<html><head><title>Foo Bar</title></head>' \
            '<body><p>Foo Bar!</p></body></html>')
        c.type = 'text/html'
        toto.content = c
        
        assert toto.content == '<html><head><title>Foo Bar' \
            '</title></head><body><p>Foo Bar!</p></body></html>'
        assert toto.content.type == 'text/html'
        assert toto.content.public_uri == '/public/test_layer/toto'
        
        toto.save()
        fetched = self.layer.pincaster.server(toto.content.public_uri)
        
        assert toto.content == fetched
    
    
    def test_linked_records(self):
        
        donald = self.layer['donald']
        donald.update({
            'first_name': 'Donald',
            'last_name': 'Duck',
        })
        donald.save()
        
        abcd = self.layer['abcd']
        
        abcd.coords = 48.512, 2.243
        abcd.update({
            'name': 'MacDonalds',
            'closed': 1,
            'address': 'blabla',
            'visits': 100000
        })
        abcd.save()
        
        donald.links['favorite_restaurant'] = abcd
        donald.save()
        
        assert donald.get('$link:favorite_restaurant', False)
        assert donald.get('$link:favorite_restaurant', False) == abcd.key
        
        # Downloads again donald
        d1 = self.layer['donald']
        a1 = d1.links['favorite_restaurant']
        
        assert d1.get('$link:favorite_restaurant', False)
        assert a1.key == abcd.key
        
        del d1
        
        # Downloads again donald, with linked records
        d2 = self.layer.get_record('donald', download_links=True)
        a2 = d2.links['favorite_restaurant']
        
        assert d2.get('$link:favorite_restaurant', False)
        assert a2.key == abcd.key
        
        del d2
    
    def test_atomicity(self):
        
        abcd = self.layer['abcd']
        abcd.coords = 48.512,2.243
        
        assert abcd == {}
        assert abcd._put_data() == {'_loc': '48.5120,2.2430'}
        
        abcd.save()
        
        assert abcd == {}
        assert abcd._put_data() == {}
        
        abcd = self.layer['abcd']

        assert abcd == {}
        assert abcd._put_data() == {}
        
        abcd.update({
            'name':'MacDonalds',
            'closed': 1,
            'address': 'blabla',
            'visits': 100000
        })

        assert abcd == {'address': 'blabla', 'name': 'MacDonalds', 'visits': 100000, 'closed': 1}
        assert abcd._put_data() == {'visits': 100000, 'name': 'MacDonalds', 'closed': 1, 'address': 'blabla'}
        
        abcd.save()

        assert abcd == {'address': 'blabla', 'name': 'MacDonalds', 'visits': 100000, 'closed': 1}
        assert abcd._put_data() == {'visits': 100000, 'name': 'MacDonalds', 'closed': 1, 'address': 'blabla'}
        
        abcd = self.layer['abcd']
        
        assert abcd == {'visits': 100000, 'name': u'MacDonalds', 'closed': 1, 'address': u'blabla'}
        assert abcd._put_data() == {'closed': 1, 'name': u'MacDonalds', 'visits': 100000, 'address': u'blabla'}
        
        del abcd['closed']
        abcd['visits'] += 127
        
        assert abcd == {'visits': 100127, 'name': u'MacDonalds', 'address': u'blabla'}
        assert abcd._put_data() == {'address': u'blabla', 'name': u'MacDonalds', '_delete:closed': 1, '_add_int:visits': 127}
        
        abcd.save()
        abcd = self.layer['abcd']
        
        assert abcd == {'name': u'MacDonalds', 'visits': 100127, 'address': u'blabla'}
        assert abcd._put_data() == {'name': u'MacDonalds', 'visits': 100127, 'address': u'blabla'}
    
    def test_around(self):
        first = self.layer['first']
        first.coords = 48.054, 12.001
        first.save()

        second = self.layer['second']
        second.coords = 48.024, 12.100
        second.save()

        third = self.layer['third']
        third.coords = 48.07, 12.0501
        third.save()

        z = self.layer['z']
        z.save()
        
        records = third.around(limit=200, radius=7000)
        
        assert len(records) == 3
        assert first in records
        assert 'first' in records
        assert first in records
        assert 'first' in records
        assert 'aze' not in records
        assert z not in records
        
        self.assertRaises(TypeError, z.around, limit=200, radius=7000)
