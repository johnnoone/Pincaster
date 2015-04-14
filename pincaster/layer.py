__all__ = ['KeySet', 'Layer', 'RecordSet']

from record import Record
from exceptions import Http404, RecordUnreachable
from utils import extract_coords
import urllib


class Layer(dict):

    __slots__ = ('name', 'pincaster', '_properties')

    def __init__(self, name, server, **kwargs):
        self.name = name
        self.pincaster = server
        self._properties = kwargs

    def save(self):
        """
        Saves the current layer.

        """

        command = self.pincaster.server
        response = command('/api/1.0/layers/%s.json' % self.name, 'POST')
        status = response['status']
        if status not in ('created', 'existing'):
            raise Exception('Unexpected status, `%s` given.' % status)

        return True

    def delete(self):
        """
        Deletes the current layer and his records.

        """

        command = self.pincaster.server
        response = command('/api/1.0/layers/%s.json' % self.name, 'DELETE')
        if response['status'] not in ('deleted',):
            raise Exception('`deleted` status expected, '
                            'but `%s` given.' % response['status'])
        return response['status']

    def get_record(self,
                   key,
                   extra=None,
                   download_links=False,
                   fail_silently=True):
        """
        Returns record `key`, from server or virtual.

        Parameters:
            key (str): Unique key
            download_links (bool): Downloads linked records when is True.
            extra (dict): Optional. Add new informations to the records,
                                    like distance...
            fail_silently (bool): Optional. When is True, always return a
                                  record, even if 404.
        Returns:
            Record
        """

        command = self.pincaster.server
        path = '/api/1.0/records/%s/%s.json' % (self.name, key)

        if download_links:
            path += '?links=1'

        try:
            response = command(path, 'GET')
            record = Record(layer=self, extra=extra, **response)
        except Http404:
            if not fail_silently:
                raise RecordUnreachable(key)
            record = Record(layer=self, extra=extra, key=key)

        return record

    def __getitem__(self, key):
        """
        Parameters:
            key (str): key
        Returns:
            Record
        """
        return self.get_record(key, fail_silently=True)

    def __delitem__(self, key):
        """
        Deletes record from layer.

        Parameters:
            key (str): key
        """
        try:
            record = self.get_record(key, fail_silently=False)
            record.delete()
        except RecordUnreachable:
            pass

    def nearby(self, coords, radius=None, limit=None, with_properties=True):
        """
        Returns records around coords.

        Parameters:
            coords (tuple): Coordinates like (x, y).
            radius (int): Distance in meters.
            limit (int): Limits fetched records.
            with_properties (bool): Fetch properties.
        Returns:
            RecordSet
        """

        coords = extract_coords(coords)
        point = '%.3f,%.3f' % coords

        params = {
            'properties': with_properties and 1 or 0
        }

        if radius:
            params['radius'] = radius
        if limit:
            params['limit'] = limit

        path = '/api/1.0/search/%s/nearby/%s.json' % (self.name, point)

        command = self.pincaster.server
        response = command(path, 'GET', data=params)
        matches = response.get('matches', [])

        return RecordSet([Record(layer=self, **m) for m in matches])

    def in_rect(self, rect, limit=None, with_properties=True):
        """
        Returns records in rect.

        Parameters:
            rect (tuple): Coordinates like (x0, y0, x1, y1).
            limit (int): Limits fetched records.
            with_properties (bool): Fetch properties.
        Returns:
            RecordSet
        """

        point = '%.3f,%.3f,%.3f,%.3f' % rect

        params = {
            'properties': with_properties and 1 or 0
        }
        if limit:
            params['limit'] = limit

        path = '/api/1.0/search/%s/in_rect/%s.json' % (self.name, point)

        command = self.pincaster.server
        response = command(path, 'GET', data=params)
        matches = response.get('matches', [])

        return RecordSet([Record(layer=self, **m) for m in matches])

    def fetch_range(self,
                    prefix,
                    limit=None,
                    keys_only=False,
                    with_properties=True):
        """
        Returns records prefixed by prefix.

        Parameters:
            prefix (str): String, like 'foo', 'foo*' ...
            limit (int): Limits fetched records.
            keys_only (bool): Returns only keys, or records?
            with_properties (with): Fetch properties.
        Returns:
            RecordSet | KeySet
        """

        path = '/api/1.0/search/%s/keys/%s.json' % (self.name,
                                                    urllib.quote(prefix))

        params = {
            'content': keys_only and 1 or 0,
            'properties': with_properties and 1 or 0
        }

        command = self.pincaster.server
        response = command(path, 'GET', data=params)

        if 'matches' in response:
            matches = response.get('matches', [])
            return RecordSet([Record(layer=self, **m) for m in matches])
        elif 'keys' in response:
            return KeySet(response['keys'])

        raise Exception('Unexcepted!')

    def fetch_records(self, prefix, limit=None, with_properties=None):
        return self.fetch_range(prefix,
                                limit=None,
                                keys_only=True,
                                with_properties=None)

    def fetch_keys(self, prefix, limit=None, with_properties=None):
        return self.fetch_range(prefix,
                                limit=None,
                                keys_only=False,
                                with_properties=None)


class RecordSet(tuple):

    def __contains__(self, other):

        try:
            key = other.key
        except AttributeError:
            if isinstance(other, (str, unicode)):
                key = other
            else:
                raise Exception('Record instance or key only')

        return any(key == item.key for item in self)


class KeySet(tuple):

    def __contains__(self, other):
        if isinstance(other, Record):
            key = other.key
            return any(key == item for item in self)
        elif isinstance(other, (str, unicode)):
            key = other
            return any(key == item for item in self)

        raise Exception('Record instance or key only')
