from collections import deque
from functools import partial, singledispatch

# generic functions on a piece of data:
# > transform((1, (2, {'foo': 3, 'bar': 'hello'})), mktrans(int, lambda i: i * 2))
# (2, (4, {'foo': 6, 'bar': 'hello'}))
# > transform((1, (2, {'foo': 3, 'bar': 'hello'})), mktrans(str, lambda i: i * 2))
# (1, (2, {'bar': 'hellohello', 'foo': 3}))
# > descend((1, (2, {'foo': 3, 'bar': 'hello'})), mktrans(int, lambda i: i * 2))
# (2, (2, {'bar': 'hello', 'foo': 3}))
# > children((1, (2, {'foo': 3, 'bar': 'hello'})))
# [1, (2, {'bar': 'hello', 'foo': 3})]
# > universe((1, (2, {'foo': 3, 'bar': 'hello'})))
# [(1, (2, {'bar': 'hello', 'foo': 3})), 1, (2, {'bar': 'hello', 'foo': 3}), 2,
#  {'bar': 'hello', 'foo': 3}, 3, 'hello']

def mktrans(t, func=None):
    """ make a function that only applies to a specific type.

    equivalent of haskell function:
    :: forall a. (a -> a) -> (forall x. Typeable x => x -> x)
    takes a transformation object and ensure it
    is only applied to the given types.

    > mktrans(int, lambda i: i * 2)("hello")
    "hello"
    > mktrans(int, lambda i: i * 2)(3)
    6
    > mktrans(int)(lambda i: i * 2)(3)
    6
    > mktrans((int, float))(lambda i: i * 2)(3.0)
    6.0

    """
    return mktranspred((lambda i: isinstance(i, t)), func=func)

def mktranspred(p, func=None):
    def decorator(func):
        def decorated(inp):
            if p(inp):
                return func(inp)
            return inp
        return decorated
    if func is not None:
        return decorator(func)
    return decorator

@singledispatch
def descend(inp, trans):
    return inp

@descend.register(tuple)
def descend_tuple(inp, trans):
    return type(inp)(trans(i) for i in inp)

@descend.register(list)
def descend_list(inp, trans):
    return type(inp)(trans(i) for i in inp)

@descend.register(type(None))
def descend_none(inp, trans):
    return None

@descend.register(dict)
def descend_dict(inp, trans):
    return type(inp)((i, trans(j)) for i, j in inp.items())

def abstract_transform(descend, inp, trans):
    return trans(descend(inp, lambda i: abstract_transform(descend, i, trans)))

# top-down transform
def abstract_transformtd(descend, inp, trans):
    return descend(trans(inp), lambda i: abstract_transformtd(descend, i, trans))

def abstract_children(descend, inp):
    results = deque()
    def collector(i):
        results.append(i)
        return i
    descend(inp, collector)
    return list(results)

def abstract_universe(descend, inp):
    results = deque()
    def collector(i):
        results.append(i)
        return i
    transformtd(inp, collector)
    return list(results)

transform = partial(abstract_transform, descend)
transform.__doc__ = """ Bottom-up transformation of data structure.

    Takes a function that transforms a single layer.
    > transform((1, (2, {'foo': 3, 'bar': 'hello'})), mktrans(int, lambda i: i * 2))
    (2, (4, {'foo': 6, 'bar': 'hello'}))

    """
transformtd = partial(abstract_transformtd, descend)
transformtd.__doc__ = """ Top-down transformation of data structure.

    Takes a function that transforms a single layer.

    """
children = partial(abstract_children, descend)
universe = partial(abstract_universe, descend)

