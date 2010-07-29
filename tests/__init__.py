import unittest

from layer import LayerTestCase
from server import ServerTestCase
from record import RecordTestCase
from search import SearchTestCase
from atomicity import AtomicityTestCase
from coords import CoordsTestCase

def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LayerTestCase))
    suite.addTest(unittest.makeSuite(ServerTestCase))
    suite.addTest(unittest.makeSuite(RecordTestCase))
    suite.addTest(unittest.makeSuite(SearchTestCase))
    suite.addTest(unittest.makeSuite(AtomicityTestCase))
    suite.addTest(unittest.makeSuite(CoordsTestCase))
    return suite
    
