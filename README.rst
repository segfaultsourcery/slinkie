Introduction
------------
This is an implementation of LINQ in Python.

Functions
---------
- between(a, b, key=None): Returns items between a and b. (Inclusive).
- count(): Consumes all items to produce a count.
- dict(key=None, value=None): Returns a dict of all items.
- exclude(items, key=None): Excludes all items based on either their identity, or a key function.
- extend(items): Yields all the items from this._items, followed by the items supplied to this function.
- filter(selector): Filter the items.
- first(selector=None): Take the first item if selector is None, otherwise take the first item where selector(item) returns true. If there are no objects, StopIteration is raised.
- first_or_none(selector=None): Take the first item if selector is None, otherwise take the first item where selector(item) returns true. If there are no objects, None is returned.
- flatten(): Flatten a two-dimensional result set into a single dimension.
- group(key): Groups all items on key.
- join(glue=''): Joins the items by glue, where glue is a string. Calls glue.join.
- last(selector=None): Take the last item if selector is None, otherwise take the first item where selector(item) returns true. If there are no objects, StopIteration is raised.
- last_or_none(selector=None): Take the first item if selector is None, otherwise take the first item where selector(item) returns true. If there are no objects, None is returned.
- len(): Consumes all items to produce a count.
- list(): Returns a list of all items.
- map(selector): Map the items.
- not_none(): Returns all items except None.
- partition(n): Takes n items and returns them in a new Slinkie. Does so until the items are consumed.
- select(selector): Map the items.
- set(): Returns a set of all items.
- skip(n): Skip n items.
- sort(key=None, reverse=False): Sorts the items by key.
- take(n): Take n items.
- tuple(): Returns a tuple of all items.
- where(selector): Filter the items.

Installation
------------
Slinkie is available on pip, so a simple "pip install slinkie" should do it.