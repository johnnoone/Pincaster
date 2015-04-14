__all__ = ['AtomicInt', 'ContentStr', 'UnixDatetime']

import datetime


class AtomicInt(int):

    def __new__(cls, value, atomicity=0):
        return int.__new__(cls, value)

    def __init__(self, value, atomicity=0):
        self.atomicity = atomicity

    def atomic_add(self, other):
        value = int.__add__(self, other)
        atom = self.atomicity + other
        return AtomicInt(value, atom)

    __add__ = atomic_add
    __radd__ = atomic_add
    __iadd__ = atomic_add

    def atomic_sub(self, other):
        value = int.__sub__(self, other)
        atom = self.atomicity - other
        return AtomicInt(value, atom)

    __sub__ = atomic_sub
    __rsub__ = atomic_sub
    __isub__ = atomic_sub

    def atomic_merge(self, other):
        value = int.__add__(self, other)
        atom = self.atomicity + getattr(other, 'atomicity', 0)
        return AtomicInt(value, atom)

    __and__ = atomic_merge
    __rand__ = atomic_merge
    __iand__ = atomic_merge


class ContentStr(str):

    def __new__(cls, content, type='text/plain', record=None):
        return str.__new__(cls, content)

    def __init__(self, content, type='text/plain', record=None):
        self.type = type
        self.record = record

    @property
    def public_uri(self):
        if self.record is None:
            return None

        return '/public/%s/%s' % (
            self.record.layer.name,
            self.record.key)


class UnixDatetime(int):

    def __new__(cls, value):
        if isinstance(value, datetime.datetime):
            value = int(value.strftime("%s"))
        return int.__new__(cls, value)

    def __init__(self, value):
        if isinstance(value, datetime.datetime):
            self._dt = value

    @property
    def datetime(self):
        if not getattr(self, '_dt', False):
            self._dt = datetime.datetime(self)
        return self._dt
