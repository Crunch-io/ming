import bson
from ming.utils import indent

class IdentityMap(object):

    def __init__(self):
        self._objects = {}

    def get(self, cls, id):
        id = _make_hashable(id)
        return self._objects.get((cls, id), None)

    def save(self, value):
        vid = getattr(value, '_id', ())
        vid = _make_hashable(vid)
        if vid is not ():
            self._objects[value.__class__, vid] = value

    def clear(self):
        self._objects = {}

    def expunge(self, obj):
        vid = getattr(obj, '_id', ())
        vid = _make_hashable(vid)
        if vid is (): return
        try:
            del self._objects[(obj.__class__, vid)]
        except KeyError:
            pass

    def __iter__(self):
        for (cls,vid), value in self._objects.iteritems():
            yield cls, vid, value

    def __repr__(self):
        l = [ '<imap (%d)>' % len(self._objects) ]
        for k,v in sorted(self._objects.iteritems()):
            l.append(indent('  %s : %s => %r'
                            % (k[0].__name__, k[1], v),
                            4))
        return '\n'.join(l)

def _make_hashable(value):
    if isinstance(value, dict):
        return _Hashable(dict, sorted(
                [ (k, _make_hashable(v)) for k,v in value.items() ]))
    if isinstance(value, list):
        return _Hashable(list, sorted(
                map(_make_hashable, value)))
    return value

class _Hashable(list):

    def __init__(self, type_, *args, **kwargs):
        self._type = type_
        super(_Hashable, self).__init__(*args, **kwargs)
    
    def __hash__(self):
        return sum(map(hash, self))
