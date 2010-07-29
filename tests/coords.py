from pincaster.utils import extract_coords
import unittest

class CoordsTestCase(unittest.TestCase):
    
    def test_extract_tuple(self):
        coords = 48, 12
        assert extract_coords(coords) == coords
        
        coords = 48.01, 12
        assert extract_coords(coords) == coords
        
        coords = 48, 12.12
        assert extract_coords(coords) == coords

        coords = -48, 12.12
        assert extract_coords(coords) == coords
        
        coords = 0, -12.12
        assert extract_coords(coords) == coords
        
        coords = 0, -12.12
        assert extract_coords(coords) == coords
        
        coords = 0, -12.12
        assert extract_coords(coords) == coords
        
        coords = 0, False
        self.assertRaises(TypeError, extract_coords, coords)
        
        coords = 0, 'toto'
        self.assertRaises(TypeError, extract_coords, coords)
    
        coords = 0, -12.12, 789
        self.assertRaises(TypeError, extract_coords, coords)
    
    def test_extract_list(self):
        coords = [48, 12]
        assert extract_coords(coords) == tuple(coords)
        
        coords = [48.01, 12]
        assert extract_coords(coords) == tuple(coords)
        
        coords = [48, 12.01]
        assert extract_coords(coords) == tuple(coords)
        
        coords = [48, 12]
        assert extract_coords(coords) == tuple(coords)
        
        coords = [48, False]
        self.assertRaises(TypeError, extract_coords, coords)
        
        coords = ['foo', False]
        self.assertRaises(TypeError, extract_coords, coords)

        coords = ['foo', False, 0.89]
        self.assertRaises(TypeError, extract_coords, coords)

    def test_extract_dict(self):
        coords = {'latitude': 48, 'longitude': 12}
        assert extract_coords(coords) == (coords['latitude'], coords['longitude'])
        
        coords = {'x': 48.08, 'y': -12}
        assert extract_coords(coords) == (coords['x'], coords['y'])
        
        coords = {'x': 'toto', 'y': -12}
        self.assertRaises(TypeError, extract_coords, coords)
        
        
        coords = {'lat': 48.08, 'lon': -12}
        assert extract_coords(coords) == (coords['lat'], coords['lon'])

        coords = {'lat': 48.08, 'lon': -12, 'foo': 123}
        assert extract_coords(coords) == (coords['lat'], coords['lon'])
    
    
    def test_extract_obj(self):
        class Mock(object):
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
        
        coords = Mock(latitude= 48, longitude= 12)
        assert extract_coords(coords) == (coords.latitude, coords.longitude)
        
        
        coords = Mock(x= 48.08, y= -12)
        assert extract_coords(coords) == (coords.x, coords.y)
        
        coords = Mock(x= 'toto', y= -12)
        self.assertRaises(TypeError, extract_coords, coords)
        
        
        coords = Mock(lat= 48.08, lon= -12)
        assert extract_coords(coords) == (coords.lat, coords.lon)
        
        coords = Mock(lat= 48.08, lon= -12, foo= 123)
        assert extract_coords(coords) == (coords.lat, coords.lon)
    
    