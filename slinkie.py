from collections import defaultdict, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import reduce
from itertools import chain

from multiprocessing import cpu_count


class Switch:
    def __init__(self, *triggers, key=None, otherwise=None):
        self._triggers = OrderedDict()
        self._key = key or (lambda it: it)
        self._otherwise = otherwise or (lambda it: it)

        for condition, callback in triggers:
            self._triggers[condition] = callback

    def evaluate(self, item):
        key = self._key
        for condition, callback in self._triggers.items():
            if condition(key(item)):
                return callback(item)
        return self._otherwise(item)

    __call__ = evaluate


class Slinkie:
    def __init__(self, items=None):
        items = items or list()
        self._items = iter(range(items) if isinstance(items, int) else items)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._items)

    def between(self, a, b, key=None):
        """
        Returns items between a and b. (Inclusive).
        """

        if key is None:
            return Slinkie(filter(lambda it: a <= it <= b, self._items))

        return Slinkie(filter(lambda it: a <= key(it) <= b, self._items))

    def exclude(self, items, key=None):
        """
        Excludes all items based on either their identity, or a key function.
        """
        if key:
            keys = list(map(key, items))
            return Slinkie(filter(lambda it: key(it) not in keys, self._items))

        return Slinkie(filter(lambda it: it not in items, self._items))

    def extend(self, items):
        """
        Yields all the items from this._items, followed by the items supplied to this function.
        """

        def _inner():
            yield from self
            yield from iter(items)

        return Slinkie(_inner())

    def filter(self, key):
        """
        Filter the items.
        """
        return Slinkie(filter(key, self._items))

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

    def flatten(self):
        """
        Flatten a two-dimensional result set into a single dimension.
        """
        return Slinkie(chain.from_iterable(self._items))

    def group(self, key):
        """
        Groups all items on key.
        """
        grouped = defaultdict(list)

        for it in self._items:
            grouped[key(it)].append(it)

        return Slinkie((k, Slinkie(v)) for k, v in grouped.items())

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

    def not_none(self):
        """
        Returns all items except None.
        """
        return Slinkie(filter(lambda it: it is not None, self._items))

    def parallelize(self, fn, number_of_threads=None):
        """
        Parallelize a function call. Number of threads defaults to your cpu count + 1.
        """

        number_of_threads = number_of_threads or (cpu_count() + 1)

        def inner():
            with ThreadPoolExecutor(number_of_threads) as tpe:
                tasks = [tpe.submit(fn, item) for item in self._items]
                for future in as_completed(tasks):
                    try:
                        yield future.result()
                    except Exception as exception:
                        yield exception

        return Slinkie(inner())

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

    def skip(self, n):
        """
        Skip n items.
        """
        for i in range(n):
            next(self._items)
        return self

    def sort(self, key=None, reverse=False):
        """
        Sorts the items by key.
        """
        return Slinkie(sorted(self._items, key=key, reverse=reverse))

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

    def transpose(self):
        """
        Transposes the contents of a Slinkie.
        """
        return Slinkie(zip(*self._items))

    # region Switching.

    def switch(self, *triggers, key=None, otherwise=None):
        """
        Switch is similar to Haskell's case. See the unit test for examples.
        """
        switch = Switch(*triggers, key=key, otherwise=otherwise)
        return Slinkie(map(switch, self._items))

    # endregion

    # region Functions consuming the slinkie.

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

    def foldl(self, fn, default=None):
        """
        Fold left. Same as reduce.
        """
        if default is None:
            default, *items = self._items
        else:
            items = self._items
        return reduce(fn, items, default)

    def foldr(self, fn, default=None):
        """
        Fold right.
        """
        if default is None:
            default, *items = reversed(list(self._items))
        else:
            items = reversed(list(self._items))
        return reduce(fn, items, default)

    def len(self):
        """
        Consumes all items to produce a count.
        """
        return sum(1 for _ in self._items)

    # endregion

    # region Functions transforming the Slinkie to another type of collection.

    def dict(self, key=None, transform=None):
        """
        Returns a dict of all items.
        """

        if key is None:
            key = lambda it: it[0]

        if transform is None:
            transform = lambda it: it[1]

        return {key(it): transform(it) for it in self._items}

    def list(self):
        """
        Returns a list of all items.
        """
        return list(self._items)

    def set(self):
        """
        Returns a set of all items.
        """
        return set(self._items)

    def str(self, glue=''):
        """
        Joins the items by glue, where glue is a string. Calls glue.join.
        """
        return glue.join(map(str, self._items))

    def tuple(self):
        """
        Returns a tuple of all items.
        """
        return tuple(self._items)

    # endregion

    # region Aliases.

    where = filter
    select = map
    count = len
    join = str
    reduce = foldl

    # endregion
