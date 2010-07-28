__all__ = ['Record']

from datetime import datetime
from exceptions import *
from containers import *


class ContentDescriptor(object):
    def __get__(self, instance, owner=None):
        return ContentStr(
            content=instance.get('$content', ''),
            type = instance.get('$content_type', 'text/plain'),
            record = instance
        )
    
    def __set__(self, instance, value):
        if isinstance(value, (ContentStr, str, unicode)):
            instance['$content_type'] = getattr(value, 'type', 'text/plain')
            instance['$content'] = str(value)
        else:
            c, t = value
            instance['$content'] = c
            instance['$content_type'] = t
    
    def __delete__(self, instance):
        instance.update({
            '$content_type': 'text/plain',
            '$content': '',
        })
    

class ExpireAtDescriptor(object):
    def __get__(self, instance, owner=None):
        """
        Returns datetime or None
        
        """
        
        e = instance._special_cmds.get('_expire_at', None)
        if isinstance(e, UnixDatetime):
            return e.datetime
        
        return None
    
    def __set__(self, instance, value):
        """
        Allows datetime or numeric value
        
        """
        
        if value in (None, False, 0, ''):
            v = 0
        else:
            v = UnixDatetime(value)
        
        instance._special_cmds['_expire_at'] = v
        
    def __delete__(self, instance):
        instance._special_cmds['_expire_at'] = 0
    
class CoordsDescriptor(object):
    def __init__(self):
        self.cache = {}
    
    def __get__(self, instance, owner=None):
        return self.cache.get(id(instance), (None, None))
    
    def __set__(self, instance, value):
        x, y = value
        self.cache[id(instance)] = x, y
        instance._special_cmds['_loc'] = '%.4f,%.4f' % (x, y)
    
    def __delete__(self, instance):
        del self.cache[id(instance)]
        del instance._special_cmds['_loc']
    

class LinkedRecords(dict):
    def __init__(self, record):
        self.record = record
    
    def __getitem__(self, link_as):
        try:
            super(LinkedRecords, self).__getitem__(link_as)
        except KeyError:
            pass
        
        __propname__ = self.l2p(link_as)
        
        if __propname__ not in self.record:
            raise KeyError(key)
        
        rkey = self.record.get(__propname__)
        
        if '$link' in self.record._srv_attrs \
            and rkey in self.record._srv_attrs['$link']:
            # prefetched, proceed
            attrs = self.record._srv_attrs['$link'][rkey]
            record = Record(layer=self.record.layer, extra={'linked_as': link_as}, **attrs)
        else:
            # download :(
            record = self.record.layer.get_record(rkey, extra={'linked_as': link_as})
        
        super(LinkedRecords, self).__setitem__(link_as, record)
        return record
    
    def __setitem__(self, link_as, record):
        __propname__ = self.l2p(link_as)
        
        if not isinstance(record, Record):
            raise Exception('Record instance only')
        
        key = record.key
        self.record._special_cmds[__propname__] = key
        self.record[__propname__] = key
        super(LinkedRecords, self).__setitem__(link_as, record)
    
    def __delitem__(self, link_as):
        __propname__ = self.l2p(link_as)
        
        self.record._special_cmds[__propname__] = ''
        del self.record[__propname__]
        super(LinkedRecords, self).__delitem__(link_as)
    
    def l2p(self, link_as):
        return '$link:%s' % link_as
    
class LinkDescriptor(object):
    def __init__(self):
        self.cache = {}
    
    def __get__(self, instance, owner=None):
        return self._inst_cache(instance)
    
    def _inst_cache(self, instance):
        pk = id(instance)
        if pk not in self.cache:
            self.cache[pk] = LinkedRecords(record=instance)
        
        return self.cache[pk]
    

class Record(dict):
    # http://www.gabes.fr/jean/2010/02/15/partie-a-trois-python-__slots__-et-metaclass/
    __slots__ = ('__dict__', 'key', 'layer', 'links', 'expire_at',
        '_initial_properties', '_special_cmds', '_svr_attrs')
    
    expire_at = ExpireAtDescriptor()
    coords = CoordsDescriptor()
    content = ContentDescriptor()
    links = LinkDescriptor()
    
    def __init__(self, key, layer, properties=None, latitude=None, longitude=None, extra=None, **kwargs):
        """
        Permet de recuperer / monter un nouveau record
        
        extra est un dict additionnel a passer au constructeur,
        au cas ou il faudrait d'autres infos
        """
        
        self.key = key
        self.layer = layer
        
        self._special_cmds = {}
        self._initial_properties = {}
        
        if properties:
            self.update(properties)
            self._initial_properties = properties.keys()
        
        if latitude is not None and longitude is not None:
            self.coords = latitude, longitude
            # a supprimer, car c'est crado
            if '_loc' in self._special_cmds:
                del self._special_cmds['_loc']
        
        self._srv_attrs = kwargs
        
    def __del__(self):
        """
        todo implemente les suppressions des caches
        """
        pass
    
    @property
    def distance(self):
        """
        Returns the distance after a nearby query
        """
        
        return self._srv_attrs.get('distance', None)
    
    def clear(self):
        self._special_cmds.update({'_delete_all':1}) 
        return super(Record, self).clear()
    
    def save(self):
        data = self._put_data()
        response = self._handle_put(data)
        
        # freeze
        for k, v in self.iteritems():
            if isinstance(v, AtomicInt):
                v.atomicity = 0
        
        self._initial_properties = self.keys()
        self._srv_attrs = response
        self._special_cmds.clear()
        
        return data, response
    
    def _put_data(self):
        p = self.copy()
        data = {}
        prop_names = p.keys()
        
        for k in self._initial_properties:
            if k not in prop_names:
                data['_delete:%s' % k] = 1

        for k, v in p.iteritems():
            if isinstance(v, AtomicInt) and v.atomicity != 0:
                data['_add_int:%s' % k] = v.atomicity
            else:
                data[k] = v
        
        # special commands 
        data.update(self._special_cmds)
        return data
    
    def _handle_put(self, data):
        path = '/api/1.0/records/%s/%s.json' % (self.layer.name, self.key)
        command = self.layer.pincaster.server
        
        response = command(path, 'PUT', data)
        if response['status'] != 'stored':
            raise Exception('Gni?')
        
        return response
    
    def delete(self):
        path = '/api/1.0/records/%s/%s.json' % (self.layer.name, self.key)
        command = self.layer.pincaster.server
        
        try:
            response = command(path, 'DELETE')
        except Http404:
            # n'existe po sur le serveur, donc on passe
            pass
        else:
            if response['status'] != 'deleted':
                raise Exception('Wrong status')
        