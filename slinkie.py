from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import chain


def _first(items):
    return next(iter(items))


class Slinkie:
    def __init__(self, items):
        self._items = iter(items)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._items)

    def consume(self, n=None):
        """
        Consume n items. If n is None, consume everything.
        """

        try:
            for _ in range(n) if n else self._items:
                next(self._items)
        except StopIteration:
            pass
        return self

    def filter(self, key):
        """
        Filter the items.
        """
        return Slinkie(filter(key, self._items))

    def map(self, transform, with_index=False, with_previous=False):
        """
        Map the items.
        """

        items = enumerate(self._items) if with_index else self._items

        if with_previous:
            # The transform function should accept two arguments, the previous and current items.
            def inner():
                previous = (None, None) if with_index else None
                for item in items:
                    yield previous, item
                    previous = item

            return Slinkie(transform(previous, item) for previous, item in inner())

        return Slinkie(map(transform, items))

    def skip(self, n):
        """
        Skip n items.
        """
        for i in range(n):
            next(self._items)
        return self

    def take(self, n):
        """
        Take n items.
        """

        def inner():
            try:
                for _ in range(n):
                    yield next(self._items)
            except StopIteration:
                return

        return Slinkie(inner())

    def first(self, key=None):
        """
        Take the first item if key is None, otherwise take the first item where key(item) returns true.
        If there are no objects, StopIteration is raised.
        """
        return next(self) if key is None else next(filter(key, self._items))

    def first_or_none(self, key=None):
        """
        Take the first item if key is None, otherwise take the first item where key(item) returns true.
        If there are no objects, None is returned.
        """
        return next(self, None) if key is None else next(filter(key, self._items), None)

    def last(self, key=None):
        """
        Take the last item if key is None, otherwise take the first item where key(item) returns true.
        If there are no objects, StopIteration is raised.
        """
        try:
            return list(self if key is None else filter(key, self._items))[-1]
        except IndexError:
            raise StopIteration()

    def last_or_none(self, key=None):
        """
        Take the first item if key is None, otherwise take the first item where key(item) returns true.
        If there are no objects, None is returned.
        """
        try:
            return self.last(key)
        except StopIteration:
            return None

    def flatten(self):
        """
        Flatten a two-dimensional result set into a single dimension.
        """
        return Slinkie(chain.from_iterable(self._items))

    def between(self, a, b, key=None):
        """
        Returns items between a and b. (Inclusive).
        """

        if key is None:
            return Slinkie(filter(lambda it: a <= it <= b, self._items))

        return Slinkie(filter(lambda it: a <= key(it) <= b, self._items))

    def not_none(self):
        """
        Returns all items except None.
        """
        return Slinkie(filter(lambda it: it is not None, self._items))

    def group(self, key):
        """
        Groups all items on key. 
        """
        grouped = defaultdict(list)

        for it in self._items:
            grouped[key(it)].append(it)

        return Slinkie((k, Slinkie(v)) for k, v in grouped.items())

    def extend(self, items):
        """
        Yields all the items from this._items, followed by the items supplied to this function.
        """

        def _inner():
            yield from self
            yield from iter(items)

        return Slinkie(_inner())

    def exclude(self, items, key=None):
        """
        Excludes all items based on either their identity, or a key function.
        """
        if key:
            keys = list(map(key, items))
            return Slinkie(filter(lambda it: key(it) not in keys, self._items))

        return Slinkie(filter(lambda it: it not in items, self._items))

    def partition(self, n):
        """
        Takes n items and returns them in a new Slinkie. Does so until the items are consumed.
        """

        def inner():
            while True:
                result = self.take(n).list()
                if not result:
                    return
                yield Slinkie(result)

        return Slinkie(inner())

    def sort(self, key=None, reverse=False):
        """
        Sorts the items by key.
        """
        return Slinkie(sorted(self._items, key=key, reverse=reverse))

    def parallelize(self, fn, threads=8):
        """
        Parallelize a function call.
        """

        def inner():
            with ThreadPoolExecutor(threads) as tpe:
                tasks = [tpe.submit(fn, item) for item in self._items]
                for future in as_completed(tasks):
                    try:
                        yield future.result()
                    except Exception as exception:
                        yield exception

        return Slinkie(inner())

    def join(self, glue=''):
        """
        Joins the items by glue, where glue is a string. Calls glue.join.
        """
        return glue.join(map(str, self._items))

    def len(self):
        """
        Consumes all items to produce a count.
        """
        return sum(1 for _ in self._items)

    def transpose(self):
        """
        Transposes the contents of a Slinkie.
        """
        return Slinkie(zip(*self._items))

    def list(self):
        """
        Returns a list of all items.
        """
        return list(self._items)

    def tuple(self):
        """
        Returns a tuple of all items.
        """
        return tuple(self._items)

    def set(self):
        """
        Returns a set of all items.
        """
        return set(self._items)

    def dict(self, key=None, transform=None):
        """
        Returns a dict of all items.
        """

        if key is None:
            key = lambda it: it[0]

        if transform is None:
            transform = lambda it: it[1]

        return {key(it): transform(it) for it in self._items}

    # Aliases
    where = filter
    select = map
    count = len
    __add__ = extend
    __sub__ = exclude
    __rshift__ = skip
