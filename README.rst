Introduction
------------
This is an implementation of LINQ in Python.

Functions
---------
- between(a, b, key=None): Returns items between a and b. (Inclusive).
- consume(n=None): Consume n items. If n is None, consume everything.
- count(): Consumes all items to produce a count.
- dict(key=None, transform=None): Returns a dict of all items.
- exclude(items, key=None): Excludes all items based on either their identity, or a key function.
- extend(items): Yields all the items from this._items, followed by the items supplied to this function.
- filter(key): Filter the items.
- first(key=None): Take the first item if key is None, otherwise take the first item where key(item) returns true. If there are no objects, StopIteration is raised.
- first_or_none(key=None): Take the first item if key is None, otherwise take the first item where key(item) returns true. If there are no objects, None is returned.
- flatten(): Flatten a two-dimensional result set into a single dimension.
- foldl(fn, default=None): Fold left. Same as reduce.
- foldr(fn, default=None): Fold right.
- group(key): Groups all items on key.
- intersperse(divider): Intersperses the items with the divider. Slinkie([1, 2, 3]).intersperse('x').list() -> [1, 'x', 2, 'x', 3].
- intersperse_items(dividers): Intersperses the items with the dividers, one by one. Slinkie([1, 2, 3, 4, 5]).intersperse_items('xy').list() -> [1, 'x', 2, 'y', 3, 'x', 4, 'y', 5].
- join(glue=''): Joins the items by glue, where glue is a string. Calls glue.join.
- last(key=None): Take the last item if key is None, otherwise take the first item where key(item) returns true. If there are no objects, StopIteration is raised.
- last_or_none(key=None): Take the first item if key is None, otherwise take the first item where key(item) returns true. If there are no objects, None is returned.
- len(): Consumes all items to produce a count.
- list(): Returns a list of all items.
- map(transform, with_index=False, with_previous=False): Map the items.
- not_none(): Returns all items except None.
- parallelize(fn, number_of_threads=None): Parallelize a function call. Number of threads defaults to your cpu count + 1.
- partition(n): Takes n items and returns them in a new Slinkie. Does so until the items are consumed.
- reduce(fn, default=None): Fold left. Same as reduce.
- select(transform, with_index=False, with_previous=False): Map the items.
- set(): Returns a set of all items.
- skip(n): Skip n items.
- sort(key=None, reverse=False): Sorts the items by key.
- str(glue=''): Joins the items by glue, where glue is a string. Calls glue.join.
- sweep(width, skip=1): Similar to itertool's pairwise, this will hand out _width_ number of items at a time, with an offset of _skip_. Slinkie(range(11)).sweep(2) yields the same result as itertools.pairwise, while .sweep(3) would give you (0, 1, 2), (1, 2, 3), ... (8, 9, 10). The last item may be None-padded if there were not _skip_ items left in the Slinkie.
- switch(*triggers, key=None, otherwise=None): Switch is similar to Haskell's case. See the unit test for examples.
- take(n): Take n items.
- tee(display=None): Every item that falls through the tee function will be displayed using the display function. If none is supplied, print is used.
- transpose(): Transposes the contents of a Slinkie.
- tuple(): Returns a tuple of all items.
- unique(key=None): Filter out items that aren't considered unique. You can optionally supply a key function to determine the identity.
- where(key): Filter the items.

Installation
------------
Slinkie is available on pip, so a simple "pip install slinkie" should do it.