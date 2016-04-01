def or_(a, b):
    if not isinstance(a, Filter) or not isinstance(b, Filter):
        raise TypeError
    return a.__or__(b)

def and_(a, b):
    return a.__and__(b)

class Filter:
    def __init__(self, dct):
        self.dct = dct

    def __or__(self, other):
        if not isinstance(other, Filter):
            raise TypeError("You can only or Filter types!")
        if '+or' in self.dct:
            return Filter({ '+or': self.dct['+or'] + [ other.dct ] })
        else:
            return Filter({ '+or': [self.dct, other.dct] })

    def __and__(self, other):
        if not isinstance(other, Filter):
            raise TypeErrand("You can only and Filter types!")
        if '+and' in self.dct:
            return Filter({ '+and': self.dct['+and'] + [ other.dct ] })
        else:
            return Filter({ '+and': [self.dct, other.dct] })

class FilterableAttribute:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return Filter({ self.name: other })

    def __ne__(self, other):
        return Filter({ self.name: { "+ne": other } })

    # "in" evaluates the return value - have to use 
    # type.contains instead
    def contains(self, other):
        return Filter({ self.name: { "+contains": other } })

    def __gt__(self, other):
        return Filter({ self.name: { "+gt": other } })

    def __lt__(self, other):
        return Filter({ self.name: { "+lt": other } })

    def __ge__(self, other):
        return Filter({ self.name: { "+gte": other } })

    def __le__(self, other):
        return Filter({ self.name: { "+lte": other } })

class FilterableMetaclass(type):
    def __init__(cls, name, bases, dct):
        if hasattr(cls, 'properties'):
            for key in cls.properties.keys():
                if cls.properties[key].filterable:
                    setattr(cls, key, FilterableAttribute(key))

        super(FilterableMetaclass, cls).__init__(name, bases, dct)
