def extract_coords(obj):
    """Extract coords from input
    
    >>> extract_point((48, 12))
    (48, 12)
    >>> extract_point({'latitude': 48, 'longitude': longitude})
    (48, 12)
    """
    
    if obj is None:
        raise TypeError('(x, y) required, None given.')
    
    def coordinify(coords):
        def validate(value):
            if isinstance(value, bool):
                raise TypeError('Wrong type, bool given.')
            
            if not isinstance(value, (int, float)):
                raise TypeError('Wrong type, %s given.' % type(value))
            
            return True
        
        try:
            x, y = coords
        except ValueError:
            raise TypeError('Not (x, y).')
            
        validate(x)
        validate(y)
        
        return x, y
    
    coords = None
    
    if getattr(obj, 'coords', False):
        return coordinify(obj.coords)
    
    attrs_pairs = (
        ('lat', 'lon'),
        ('latitude', 'longitude'),
        ('x', 'y'),
    )
    
    # if it's an instance with attributes ...
    for x, y in attrs_pairs:
        try:
            if getattr(obj, x, False) and getattr(obj, y, False):
                coords = getattr(obj, x), getattr(obj, y)
                return coordinify(coords)
        except ValueError:
            pass
    
    # if it's an instance with items ...
    for x, y in attrs_pairs:
        try:
            if x in obj and y in obj:
                coords = obj[x], obj[y]
                return coordinify(coords)
        except ValueError:
            pass
    
    # let's say it's a coords
    coords = obj
    return coordinify(coords)
    
