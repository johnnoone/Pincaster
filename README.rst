=========
Pincaster
=========

This is the Python interface to the Pincaster server store.


Installation
============

#. Download the package in your computer. (https://github.com/johnnoone/Pincaster)

#. Run ``python setup.py install`` and you're done.


Usage
=====

Atomic updates
--------------

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
    ...     'what': 'city',
    ...     'population': 2193031
    ... })
    >>> paris
    {'what': 'city', 'population': 2193031}
    >>> paris.coords = 48.856667, 2.350833
    >>> paris.save()
    True
    
Time passes, a new birth in Paris, atomicaly increment population

::
    
    >>> paris = france['paris']
    >>> paris['population'] += 1
    >>> paris
    {'what': 'city', 'population': 2193032}
    >>> paris.save()
    True
    >>> paris['population']
    2193032


Linked records
--------------

::
    
    >>> diznyland = pincaster['diznyland']
    >>> diznyland.save()
    True
    >>> donald = diznyland['donald']
    >>> donald.update({
    ...     'first_name': 'Donald',
    ...     'last_name': 'Duck',
    ... })
    >>> donald.save()
    True

    >>> abcd = diznyland['abcd']
    >>> abcd.coords = 48.512, 2.243
    >>> abcd.update({
    ...     'name': 'MacDonalds',
    ...     'closed': 1,
    ...     'address': 'blabla',
    ...     'visits': 100000
    ... })
    >>> abcd.save()
    True
    >>> donald.links['favorite_restaurant'] = abcd
    >>> donald.save()
    True
    >>> donald
    {'first_name': 'Donald', 'last_name': 'Duck', '$link:favorite_restaurant': 'abcd'}
    >>> donald['$link:favorite_restaurant']
    abcd
    >>> donald.links['favorite_restaurant']
    {'visits': 100000, 'name': u'MacDonalds', 'closed': 1, 'address': u'blabla'}

    >>> # Downloads again donald
    >>> d1 = diznyland['donald']
    >>> a1 = d1.links['favorite_restaurant']
    >>> d1
    {'first_name': u'Donald', 'last_name': u'Duck', '$link:favorite_restaurant': u'abcd'}
    >>> d1['$link:favorite_restaurant']
    abcd
    >>> d1.links['favorite_restaurant']
    {'visits': 100000, 'name': u'MacDonalds', 'closed': 1, 'address': u'blabla'}
    >>> del d1

    >>> # Downloads again donald, with linked records
    >>> d2 = diznyland.get_record('donald', download_links=True)
    >>> a2 = d2.links['favorite_restaurant']
    >>> d2['$link:favorite_restaurant']
    abcd
    >>> del d2


Geographic search
-----------------

Rock around a record

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
    
