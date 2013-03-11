from functools import wraps
from exceptions import DataMinerError, DataSourceNotReachableException, DataNotFoundException

def with_exceptions(fn):
    @wraps(fn)
    def _with_exceptions(*argt, **argd):
        try:
            ret = fn(*argt, **argd)
            return ret
        except KeyError, e:
            raise DataNotFoundException("Could not find appropriate data in datasource for %s (%s, %s)" % (argt, fn.__doc__, e))
        except IOError, e:
            raise DataSourceNotReachableException("Could not reach datasource (%s): %s", (fn.__doc__, e))
        except Exception, e:
            raise DataMinerError("Unknown error in %s miner: %s", (fn.__doc__, e))

    return _with_exceptions