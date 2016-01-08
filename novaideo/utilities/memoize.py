_marker = object()


class Memojito(object):
    propname = '_memojito_'

    def memoize(self, func):

        def memogetter(*args, **kwargs):
            inst = args[0]
            cache = getattr(inst, self.propname, _marker)
            if cache is _marker:
                setattr(inst, self.propname, dict())
                cache = getattr(inst, self.propname)

            # XXX this could be potentially big, a custom key should
            # be used if the arguments are expected to be big

            key = (func.__name__, args, frozenset(kwargs.items()))
            val = cache.get(key, _marker)
            if val is _marker:
                val = func(*args, **kwargs)
                cache[key] = val
                setattr(inst, self.propname, cache)
            return val
        return memogetter

_m = Memojito()
memoize = _m.memoize
