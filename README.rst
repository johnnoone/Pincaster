=========
Pincaster
=========

This is the Python interface to the Pincaster server store.


Installation
============

#. Download the package in your computer.

#. Run ``python setup.py install`` and you're done.


Usage
=====

::
    
    >>> from pincaster import *
    >>> pincaster = Pincaster('127.0.0.1', 4269)
    >>> france = Layer('france', pincaster)
    >>> france.save()
    True
    
Create Paris

::
    
    >>> paris = Record('paris', france)
    >>> paris.update({
    ...   'what': 'city',
    ...   'population': 2193031
    ... })
    >>> paris
    {'what': 'city', 'population': 2193031}
    >>> paris.coords = 48.856667, 2.350833
    >>> paris.save()
    True
    
Time passes, a new birth in Paris, atomicaly increment population

::
    
    >>> pincaster = Pincaster('127.0.0.1', 4269)
    >>> france =  pincaster['france']
    >>> paris = france['paris']
    >>> paris['population'] += 1
    >>> paris
    {'what': 'city', 'population': 2193032}
    >>> paris.save()
    True
    >>> paris['population']
    2193032


Found search

::
    
    >>> numbers = pincaster['numbers']
    >>> numbers.save()
    True
    
    >>> first = numbers['first']
    >>> first['name'] = 'Foo'
    >>> first.coords = 48.054, 12.001
    >>> first.save()
    True
    >>> first
    {'name': 'Foo'}
    >>> first.coords
    (48.054000000000002, 12.000999999999999)
    
    >>> second = numbers['second']
    >>> second['name'] = 'Bar'
    >>> second.coords = 48.024, 12.100
    >>> second.save()
    True
    >>> second
    {'name': 'Bar'}
    >>> second.coords
    (48.024000000000001, 12.1)
    
    >>> third = numbers['third']
    >>> third['name'] = 'Baz'
    >>> third.coords = 48.07, 12.0501
    >>> third.save()
    True
    >>> third
    {'name': 'Baz'}
    >>> third.coords
    (48.07, 12.0501)
    
    >>> records = third.around(limit=200, radius=7000)
    >>> records
    ({'name': u'Foo'}, {'name': u'Bar'}, {'name': u'Baz'})
    
