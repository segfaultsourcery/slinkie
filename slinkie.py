from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import reduce
from itertools import chain, cycle

from multiprocessing import cpu_count


class Slinkie:
    def __init__(self, items=None):
        items = items or list()
        self._items = iter(range(items) if isinstance(items, int) else items)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._items)

    def all(self, key=None):
        """
        Consumes the whole slinkie to find if every item is truthy.
        """
        if key:
            return all(map(key, self._items))
        return all(self._items)

    def any(self, key=None):
        """
        Consumes the slinkie until it finds a truthy item.
        """
        if key:
            return any(map(key, self._items))
        return any(self._items)

    def between(self, a, b, key=None):
        """
        Returns items between a and b. (Inclusive).
        """
        if key:
            return Slinkie(filter(lambda it: a <= key(it) <= b, self._items))

        return Slinkie(filter(lambda it: a <= it <= b, self._items))

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

    def intersperse(self, divider):
        """
        Intersperses the items with the divider.
        Slinkie([1, 2, 3]).intersperse('x').list() -> [1, 'x', 2, 'x', 3].
        """

        def _inner():
            yield next(self._items)
            for item in self._items:
                yield divider
                yield item

        return Slinkie(_inner())

    def intersperse_items(self, dividers):
        """
        Intersperses the items with the dividers, one by one.
        Slinkie([1, 2, 3, 4, 5]).intersperse_items(['x', 'y']).list() -> [1, 'x', 2, 'y', 3, 'x', 4, 'y', 5].
        """

        def _inner():
            _dividers = cycle(dividers)
            yield next(self._items)
            for item in self._items:
                yield next(_dividers)
                yield item

        return Slinkie(_inner())

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
        Take the last item if key is None, otherwise take the last item where key(item) returns true.
        If there are no matching objects, None is returned.
        """
        try:
            return self.last(key)
        except StopIteration:
            return None

    def map(self, transform, with_index=False):
        """
        Map the items.
        """
        items = enumerate(self._items) if with_index else self._items
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

        def _inner():
            with ThreadPoolExecutor(number_of_threads) as tpe:
                tasks = [tpe.submit(fn, item) for item in self._items]
                for future in as_completed(tasks):
                    try:
                        yield future.result()
                    except Exception as exception:
                        yield exception

        return Slinkie(_inner())

    def partition(self, n):
        """
        Takes n items and returns them in a new Slinkie. Does so until the items are consumed.
        """

        def _inner():
            while True:
                result = self.take(n).list()
                if not result:
                    return
                yield Slinkie(result)

        return Slinkie(_inner())

    def reverse(self):
        """
        Reverses the order of the Slinkie.
        """
        return Slinkie(reversed(self.tuple()))

    __reversed__ = reverse

    def sfilter(self, key):
        """
        Filter the items, uses the splat operator on the key function, just like smap.
        """
        return Slinkie(filter(lambda it: key(*it), self._items))

    def sweep(self, width, step=1):
        """
        Similar to itertools' pairwise, this will hand out _width_ number of items at a time, with an offset of _step_.
        Slinkie(range(11)).sweep(2) yields the same result as itertools.pairwise, while .sweep(3) would give you
        (0, 1, 2), (1, 2, 3), ... (8, 9, 10).
        The last item may be None-padded if there were not _step_ items left in the Slinkie.
        """

        def _inner():
            items = self.take(width)
            current = deque(items, maxlen=width)
            while items:
                yield tuple(current)
                items = self.take(step).tuple()
                current.extend(items)
                if items and len(items) < step:
                    current.extend([None] * (step - len(items)))

        return Slinkie(_inner())

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

    def split(self, number_of_slinkies=2):
        """
        Split the items into smaller slinkies. Items are divided using round robin.
        """

        if number_of_slinkies <= 1:
            return self,

        collections = [deque() for _ in range(number_of_slinkies)]

        def _add_items():
            try:
                for collection in collections:
                    item = next(self._items)
                    collection.append(item)
            except StopIteration:
                pass

        def _sub_sequence(collection_index):
            _add_items()

            while collections[collection_index]:
                _add_items()
                yield collections[collection_index].popleft()

        def _inner():
            for i in range(number_of_slinkies):
                yield Slinkie(_sub_sequence(i))

        return Slinkie(_inner())

    def smap(self, transform):
        """
        Map the splat of the items.
        """
        return Slinkie(map(lambda it: transform(*it), self._items))

    def take(self, n):
        """
        Take n items.
        """

        def _inner():
            try:
                for _ in range(n):
                    yield next(self._items)
            except StopIteration:
                return

        return Slinkie(_inner())

    def tee(self, display=None):
        """
        Every item that falls through the tee function will be displayed using the display function.
        If none is supplied, print is used.
        """
        display = display or print

        def _inner():
            for item in self._items:
                display(item)
                yield item

        return Slinkie(_inner())

    def then(self, fn):
        """
        Takes a function that takes a slinkie as its only argument, and returns a collection.
        The collection is then wrapped in another slinkie.
        """
        return Slinkie(fn(self))

    def transpose(self):
        """
        Transposes the contents of a Slinkie.
        """
        return Slinkie(zip(*self._items))

    def unique(self, key=None):
        """
        Filter out items that aren't considered unique.
        You can optionally supply a key function to determine the identity.
        """

        def _inner():
            seen = set()

            if key:
                for item in self._items:
                    _item = key(item)
                    if key(item) not in seen:
                        seen.add(_item)
                        yield item
                return

            for item in self._items:
                if item not in seen:
                    seen.add(item)
                    yield item

        return Slinkie(_inner())

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

    def dict(self, key, transform=None):
        """
        Returns a dict of all items.
        """

        if transform is None:
            return {key(it): it for it in self._items}

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


# region Utils

def first(items):
    """
    Gets the first item from a collection.
    """
    return items[0]


def second(items):
    """
    Gets the second item from a collection.
    """
    return items[1]


def third(items):
    """
    Gets the third item from a collection.
    """
    return items[2]


def by_key(key):
    """
    Returns a function that gets an item by the specified key.

    Example:
    (
        Slinkie(items)
            .sort(by_key('date'))
    )
    """

    return lambda items: items[key]


def by_keys(*keys):
    """
    Returns a function that gets a tuple of items by the specified keys.

    Example:
    (
        Slinkie(people)
            .sort(by_keys('age', 'name'))
            .map(by_keys('name', 'phone_number'))
    )
    """

    return lambda items: tuple(items[key] for key in keys)

# endregion
