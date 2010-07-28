import unittest

from layer import LayerTestCase
from server import ServerTestCase
from record import RecordTestCase
from search import SearchTestCase
from atomicity import AtomicityTestCase

def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LayerTestCase))
    suite.addTest(unittest.makeSuite(ServerTestCase))
    suite.addTest(unittest.makeSuite(RecordTestCase))
    suite.addTest(unittest.makeSuite(SearchTestCase))
    suite.addTest(unittest.makeSuite(AtomicityTestCase))
    return suite
    
