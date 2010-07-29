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
