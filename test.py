import unittest
from functools import partial
from operator import mul

from slinkie import Slinkie


class TestSlinkie(unittest.TestCase):
    ITEMS = list(range(21))

    def test_between(self):
        actual = Slinkie(self.ITEMS).between(5, 8).list()
        expected = [5, 6, 7, 8]
        self.assertSequenceEqual(actual, expected)

        actual = Slinkie(self.ITEMS) \
            .map(lambda it: {'id': it}) \
            .between(5, 8, key=lambda it: it['id']) \
            .list()

        expected = [{'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}]
        self.assertSequenceEqual(actual, expected)

    def test_count(self):
        actual = Slinkie(self.ITEMS).count()
        expected = len(self.ITEMS)
        self.assertEqual(actual, expected)

    def test_dict(self):
        def _classify(it):
            return 'even' if it & 1 == 0 else 'uneven'

        actual = Slinkie(self.ITEMS) \
            .group(_classify) \
            .dict(transform=lambda it: it[1].tuple())

        expected_evens = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
        expected_unevens = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19)

        self.assertTupleEqual(actual['even'], expected_evens)
        self.assertTupleEqual(actual['uneven'], expected_unevens)

    def test_exclude(self):
        to_exclude = list(range(5, 11))
        actual = Slinkie(self.ITEMS).exclude(to_exclude).tuple()
        expected = (0, 1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
        self.assertTupleEqual(actual, expected)

        to_exclude = [{'id': 3}]
        actual = Slinkie(self.ITEMS) \
            .take(5) \
            .map(lambda it: {'id': it}) \
            .exclude(to_exclude, key=lambda it: it['id']) \
            .tuple()

        expected = ({'id': 0}, {'id': 1}, {'id': 2}, {'id': 4})
        self.assertTupleEqual(actual, expected)

    def test_extend(self):
        list1 = (1, 2, 3)
        list2 = (4, 5, 6)
        actual = Slinkie(list1).extend(list2).tuple()
        expected = (1, 2, 3, 4, 5, 6)
        self.assertTupleEqual(actual, expected)

    def test_filter(self):
        def only_even(it):
            return it & 1 == 0

        actual = Slinkie(self.ITEMS).filter(only_even).tuple()
        expected = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)

        self.assertTupleEqual(actual, expected)

    def test_first(self):
        actual = Slinkie(self.ITEMS).first()
        expected = self.ITEMS[0]
        self.assertEqual(actual, expected)

        with self.assertRaises(StopIteration):
            Slinkie([]).first()

    def test_first_or_none(self):
        actual = Slinkie(self.ITEMS).first_or_none()
        expected = self.ITEMS[0]
        self.assertEqual(actual, expected)

        actual = Slinkie([]).first_or_none()
        expected = None
        self.assertEqual(actual, expected)

    def test_flatten(self):
        items = ((1, 2), (3, 4))
        actual = Slinkie(items).flatten().tuple()
        expected = (1, 2, 3, 4)
        self.assertTupleEqual(actual, expected)

    def test_group(self):
        def _classify(it):
            return 'even' if it & 1 == 0 else 'uneven'

        actual = Slinkie(self.ITEMS) \
            .group(_classify) \
            .dict(transform=lambda it: it[1].tuple())

        expected_evens = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
        expected_unevens = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19)

        self.assertTupleEqual(actual['even'], expected_evens)
        self.assertTupleEqual(actual['uneven'], expected_unevens)

    def test_join(self):
        items = ('a', 'b', 12)
        actual = Slinkie(items).join('-')
        expected = 'a-b-12'
        self.assertEqual(actual, expected)

    def test_last(self):
        actual = Slinkie(self.ITEMS).last()
        expected = self.ITEMS[-1]
        self.assertEqual(actual, expected)

        with self.assertRaises(StopIteration):
            Slinkie([]).last()

    def test_last_or_none(self):
        actual = Slinkie(self.ITEMS).last_or_none()
        expected = self.ITEMS[-1]
        self.assertEqual(actual, expected)

        actual = Slinkie([]).last_or_none()
        expected = None
        self.assertEqual(actual, expected)

    def test_len(self):
        actual = Slinkie(self.ITEMS).len()
        expected = len(self.ITEMS)
        self.assertEqual(actual, expected)

    def test_list(self):
        actual = Slinkie(self.ITEMS).list()
        expected = list(self.ITEMS)
        self.assertListEqual(actual, expected)

    def test_map(self):
        doublify = partial(mul, 2)
        actual = Slinkie(self.ITEMS).take(3).map(doublify).tuple()
        expected = (0, 2, 4)
        self.assertTupleEqual(actual, expected)

    def test_not_none(self):
        items = (1, 2, None, 3, None)
        actual = Slinkie(items).not_none().tuple()
        expected = (1, 2, 3)
        self.assertTupleEqual(actual, expected)

    def test_partition(self):
        actual = Slinkie(self.ITEMS).partition(3).first().tuple()
        expected = (0, 1, 2)
        self.assertEqual(actual, expected)

    def test_select(self):
        _doublify = partial(mul, 2)
        actual = Slinkie(self.ITEMS).take(3).select(_doublify).tuple()
        expected = (0, 2, 4)
        self.assertTupleEqual(actual, expected)

    def test_set(self):
        actual = Slinkie(self.ITEMS).set()
        expected = set(self.ITEMS)
        self.assertSetEqual(actual, expected)

    def test_skip(self):
        actual = Slinkie(self.ITEMS).skip(1).first()
        expected = 1
        self.assertEqual(actual, expected)

    def test_sort(self):
        items = (5, 1, 7, 2)
        actual = Slinkie(items).sort().tuple()
        expected = tuple(sorted(items))
        self.assertTupleEqual(actual, expected)

        actual = Slinkie(items).sort(lambda it: it).tuple()
        self.assertTupleEqual(actual, expected)

    def test_take(self):
        actual = Slinkie(self.ITEMS).take(3).list()
        expected = [0, 1, 2]
        self.assertSequenceEqual(actual, expected)

    def test_transpose(self):
        items = ((1, 2), (3, 4))
        actual = Slinkie(items).transpose().tuple()
        expected = list(zip(*items))
        self.assertSequenceEqual(actual, expected)

        items = '1a2b3c'
        actual = Slinkie(items).partition(2).transpose().tuple()
        expected = (('1', '2', '3'), ('a', 'b', 'c'))
        self.assertSequenceEqual(actual, expected)

    def test_tuple(self):
        actual = Slinkie(self.ITEMS).tuple()
        expected = tuple(self.ITEMS)
        self.assertTupleEqual(actual, expected)

    def test_where(self):
        def only_even(it):
            return it & 1 == 0

        actual = Slinkie(self.ITEMS).where(only_even).tuple()
        expected = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)

        self.assertTupleEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
