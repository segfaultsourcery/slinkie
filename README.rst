Introduction
------------
This is an implementation of LINQ in Python.

Functions
---------
- between: Returns items between a and b. (Inclusive).
- count: Consumes all items to produce a count.
- dict: Returns a dict of all items.
- exclude: Excludes all items based on either their identity, or a key function.
- extend: Yields all the items from this._items, followed by the items supplied to this function.
- filter: Filter the items.
- first: Take the first item if selector is None, otherwise take the first item where selector(item) returns true. If there are no objects, StopIteration is raised.
- first_or_none: Take the first item if selector is None, otherwise take the first item where selector(item) returns true. If there are no objects, None is returned.
- flatten: Flatten a two-dimensional result set into a single dimension.
- group: Groups all items on key.
- join: Joins the items by glue, where glue is a string. Calls glue.join.
- last: Take the last item if selector is None, otherwise take the first item where selector(item) returns true. If there are no objects, StopIteration is raised.
- last_or_none: Take the first item if selector is None, otherwise take the first item where selector(item) returns true. If there are no objects, None is returned.
- len: Consumes all items to produce a count.
- list: Returns a list of all items.
- map: Map the items.
- not_none: Returns all items except None.
- partition: Takes n items and returns them in a new Slinkie. Does so until the items are consumed.
- select: Map the items.
- set: Returns a set of all items.
- skip: Skip n items.
- sort: Sorts the items by key.
- take: Take n items.
- tuple: Returns a tuple of all items.
- where: Filter the items.

Installation
------------
Slinkie is available on pip, so a simple "pip install slinkie" should do it.