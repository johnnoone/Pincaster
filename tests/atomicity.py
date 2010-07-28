from pincaster.atomicity import *
import unittest

class AtomicityTestCase(unittest.TestCase):
    def test_atomic_add(self):
        
        a = AtomicInt(10)
        
        assert a == 10
        assert a.atomicity == 0

        b = a.atomic_add(5)
        
        assert b == 15
        assert b.atomicity == 5

        c = b.atomic_add(1)

        assert c == 16
        assert c.atomicity == 6

    def test_add(self):
        
        a = AtomicInt(10)
        
        assert a == 10
        assert a.atomicity == 0

        b = a + 5

        assert b == 15
        assert b.atomicity == 5

        c = b + 1

        assert c == 16
        assert c.atomicity == 6
    
    def test_radd(self):
        
        a = AtomicInt(10)
        
        assert a == 10
        assert a.atomicity == 0

        b = 5 + a

        assert b == 15
        assert b.atomicity == 5

        c = 1 + b

        assert c == 16
        assert c.atomicity == 6

    def test_int_iadd(self):
        
        a = AtomicInt(10)
        
        assert a == 10
        assert a.atomicity == 0

        a += 5

        assert a == 15
        assert a.atomicity == 5

        a += 1

        assert a == 16
        assert a.atomicity == 6


    def test_atomic_sub(self):
        
        a = AtomicInt(10)
        
        assert a == 10
        assert a.atomicity == 0

        b = a.atomic_sub(5)

        assert b == 5
        assert b.atomicity == -5

        c = b.atomic_sub(1)

        assert c == 4
        assert c.atomicity == -6
    
    def test_sub(self):
        
        a = AtomicInt(10)
        
        assert a == 10
        assert a.atomicity == 0

        b = a - 5

        assert b == 5
        assert b.atomicity == -5

        c = b - 1

        assert c == 4
        assert c.atomicity == -6
    

    def test_int_rsub(self):
        
        a = AtomicInt(10)
        
        assert a == 10
        assert a.atomicity == 0

        b = 5 - a

        assert b == 5
        assert b.atomicity == -5

        c = 1 - b

        assert c == 4
        assert c.atomicity == -6

    def test_int_isub(self):
        
        a = AtomicInt(10)
        
        assert a == 10
        assert a.atomicity == 0

        a -= 5

        assert a == 5
        assert a.atomicity == -5

        a -= 1

        assert a == 4
        assert a.atomicity == -6
    
    def test_atomic_merge(self):
        
        a = AtomicInt(10)
        b = a.atomic_merge(5)
        
        assert b == 15
        assert b.atomicity == 0

        c = b.atomic_merge(AtomicInt(1, 10))
        
        assert c == 16
        assert c.atomicity == 10

        d = c.atomic_merge(AtomicInt(-5, 4))
        
        assert d == 11
        assert d.atomicity == 14
    
    def test_and(self):
        
        a = AtomicInt(10)
        b = a & 5
        
        assert b == 15
        assert b.atomicity == 0

        c = b & AtomicInt(1, 10)
        
        assert c == 16
        assert c.atomicity == 10

        d = c & AtomicInt(-5, 4)
        
        assert d == 11
        assert d.atomicity == 14
    
    def test_rand(self):
        
        a = AtomicInt(10)
        b = 5 & a
        
        assert b == 15
        assert b.atomicity == 0

        c = AtomicInt(1, 10) & b
        
        assert c == 16
        assert c.atomicity == 10

        d = AtomicInt(-5, 4) & c
        
        assert d == 11
        assert d.atomicity == 14
    
    def test_iand(self):
        
        a = AtomicInt(10)
        a &= 5
        
        assert a == 15
        assert a.atomicity == 0

        a &= AtomicInt(1, 10)
        
        assert a == 16
        assert a.atomicity == 10

        a &= AtomicInt(-5, 4)
        
        assert a == 11
        assert a.atomicity == 14
    
