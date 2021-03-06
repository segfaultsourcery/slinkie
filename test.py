import unittest
from functools import partial, reduce
from operator import mul, sub
from time import sleep

from slinkie import Slinkie, first, second, third, by_key, by_keys


class TestSlinkie(unittest.TestCase):
    ITEMS = list(range(21))

    def test_all(self):
        items = [True, 'a', 1]
        actual = Slinkie(items).all()
        expected = True
        self.assertEqual(actual, expected)

        items = [True, '', 1]
        actual = Slinkie(items).all()
        expected = False
        self.assertEqual(actual, expected)

        items = []
        actual = Slinkie(items).all()
        expected = True
        self.assertEqual(actual, expected)

    def test_any(self):
        items = [True, 'a', 1]
        actual = Slinkie(items).any()
        expected = True
        self.assertEqual(actual, expected)

        items = [True, '', 1]
        actual = Slinkie(items).any()
        expected = True
        self.assertEqual(actual, expected)

        items = []
        actual = Slinkie(items).any()
        expected = False
        self.assertEqual(actual, expected)

    def test_between(self):
        actual = Slinkie(self.ITEMS).between(5, 8).list()
        expected = [5, 6, 7, 8]
        self.assertSequenceEqual(actual, expected)

        actual = (
            Slinkie(self.ITEMS)
                .map(lambda it: {'id': it})
                .between(5, 8, key=lambda it: it['id'])
                .list()
        )

        expected = [{'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}]
        self.assertSequenceEqual(actual, expected)

    def test_consume(self):
        actual = Slinkie(self.ITEMS).consume().len()
        expected = 0
        self.assertEqual(actual, expected)

        actual = Slinkie(self.ITEMS).consume(10).len()
        expected = 11
        self.assertEqual(actual, expected)

    def test_count(self):
        actual = Slinkie(self.ITEMS).count()
        expected = len(self.ITEMS)
        self.assertEqual(actual, expected)

    def test_dict(self):
        def _classify(it):
            return 'even' if it & 1 == 0 else 'uneven'

        actual = (
            Slinkie(self.ITEMS)
                .group(_classify)
                .dict(
                key=lambda it: it[0],
                transform=lambda it: it[1].tuple()))

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
        actual = (
            Slinkie(self.ITEMS)
                .take(5)
                .map(lambda it: {'id': it})
                .exclude(to_exclude, key=by_key('id'))
                .tuple()
        )

        expected = ({'id': 0}, {'id': 1}, {'id': 2}, {'id': 4})
        self.assertTupleEqual(actual, expected)

    def test_extend(self):
        list1 = (1, 2, 3)
        list2 = (4, 5, 6)
        actual = Slinkie(list1).extend(list2).tuple()
        expected = (1, 2, 3, 4, 5, 6)
        self.assertTupleEqual(actual, expected)

        actual = Slinkie().extend('abc').extend('def').str()
        expected = 'abcdef'
        self.assertEqual(actual, expected)

        actual = Slinkie(3).extend('abc').str()
        expected = '012abc'
        self.assertEqual(actual, expected)

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

    def test_foldl(self):
        actual = Slinkie(self.ITEMS).foldl(sub)
        expected = reduce(sub, self.ITEMS)
        self.assertEqual(actual, expected)

    def test_foldr(self):
        items = list(range(3))
        actual = Slinkie(items).foldr(sub)
        expected = reduce(sub, reversed(items))
        self.assertEqual(actual, expected)

    def test_group(self):
        def _classify(it):
            return 'even' if it & 1 == 0 else 'uneven'

        actual = (
            Slinkie(self.ITEMS)
                .group(_classify)
                .dict(
                key=lambda it: it[0],
                transform=lambda it: it[1].tuple()))

        expected_evens = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
        expected_unevens = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19)

        self.assertTupleEqual(actual['even'], expected_evens)
        self.assertTupleEqual(actual['uneven'], expected_unevens)

    def test_intersperse(self):
        actual = Slinkie([1, 2, 3]).intersperse('x').list()
        expected = [1, 'x', 2, 'x', 3]
        self.assertListEqual(actual, expected)

        actual = Slinkie([1]).intersperse('x').list()
        expected = [1]
        self.assertListEqual(actual, expected)

        actual = Slinkie([]).intersperse('x').list()
        expected = []
        self.assertListEqual(actual, expected)

    def test_intersperse_items(self):
        actual = Slinkie([1, 2, 3, 4, 5]).intersperse_items('xy').list()
        expected = [1, 'x', 2, 'y', 3, 'x', 4, 'y', 5]
        self.assertListEqual(actual, expected)

        actual = Slinkie([1]).intersperse_items('xy').list()
        expected = [1]
        self.assertListEqual(actual, expected)

        actual = Slinkie([]).intersperse_items('xy').list()
        expected = []
        self.assertListEqual(actual, expected)

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
        _doublify = partial(mul, 2)

        # Double a series of numbers.
        actual = Slinkie(self.ITEMS).take(3).map(_doublify).tuple()
        expected = (0, 2, 4)
        self.assertTupleEqual(actual, expected)

        # Double a series of numbers, add index numbers.
        _doublify = partial(mul, 2)
        actual = (
            Slinkie(self.ITEMS)
                .take(3)
                .map((lambda pair: (pair[0], _doublify(pair[1]))), with_index=True)
                .tuple()
        )
        expected = ((0, 0), (1, 2), (2, 4))
        self.assertTupleEqual(actual, expected)

    def test_not_none(self):
        items = (1, 2, None, 3, None)
        actual = Slinkie(items).not_none().tuple()
        expected = (1, 2, 3)
        self.assertTupleEqual(actual, expected)

    def test_parallelize(self):
        def _wait(number):
            sleep(number / 10.0)
            return number

        numbers = (7, 2, 1, 4, 2, 5, 1, 1, 2, 3)
        actual = Slinkie(numbers).parallelize(_wait, len(numbers)).list()
        expected = sorted(numbers)

        self.assertSequenceEqual(actual, expected)

    def test_partition(self):
        actual = Slinkie(self.ITEMS).partition(3).first().tuple()
        expected = (0, 1, 2)
        self.assertEqual(actual, expected)

    def test_reverse(self):
        actual = Slinkie(self.ITEMS).take(3).reverse().tuple()
        expected = (2, 1, 0)
        self.assertEqual(actual, expected)

        actual = tuple(reversed(Slinkie(self.ITEMS).take(3)))
        expected = (2, 1, 0)
        self.assertEqual(actual, expected)

    def test_sweep(self):
        numbers = list(range(6))

        actual = Slinkie(numbers).sweep(2).list()
        expected = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
        self.assertSequenceEqual(actual, expected)

        actual = Slinkie(numbers).sweep(3).list()
        expected = [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]
        self.assertSequenceEqual(actual, expected)

        actual = Slinkie(numbers).sweep(3, 2).list()
        expected = [(0, 1, 2), (2, 3, 4), (4, 5, None)]
        self.assertSequenceEqual(actual, expected)

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

    def test_split(self):
        actual = Slinkie(range(9)).split(3).map(list).list()
        expected = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
        self.assertEqual(actual, expected)

    def test_smap(self):
        actual = (
            Slinkie([(1, 2)])
                .smap(lambda a, b: a + b)
                .first()
        )
        expected = 3
        self.assertEqual(actual, expected)

        actual = (
            Slinkie((1, 2, 3))
                .sweep(2)
                .smap(lambda a, b: a + b)
                .tuple()
        )
        expected = (3, 5)
        self.assertEqual(actual, expected)

    def test_filter(self):

        def sum_is_even(a, b, c):
            return (a + b + c) & 1 == 0

        actual = (
            Slinkie(range(0, 6))
                .sweep(3)
                .sfilter(sum_is_even)
                .tuple()
        )

        expected = ((1, 2, 3), (3, 4, 5))

        self.assertTupleEqual(actual, expected)

    def test_take(self):
        actual = Slinkie(self.ITEMS).take(3).list()
        expected = [0, 1, 2]
        self.assertSequenceEqual(actual, expected)

    def test_tee(self):
        actual = []

        def _tee(item):
            print(item)
            actual.append(item)
            return item

        Slinkie(self.ITEMS).tee(_tee).take(3).consume()
        expected = [0, 1, 2]
        self.assertSequenceEqual(actual, expected)

    def test_then(self):
        items = (1, 2, 3, 4)
        actual = (
            Slinkie(items)
                .then(lambda it: reversed(it.list()))
                .list()
        )
        expected = list(reversed(items))
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

    def test_unique(self):
        items = [1, 1, 2, 7, 4, 4, 5, 1]
        actual = Slinkie(items).unique().sort().list()
        expected = sorted(set(items))
        self.assertSequenceEqual(actual, expected)

        actual = Slinkie(items).unique(key=lambda it: it & 1 == 0).sort().list()
        expected = [1, 2]
        self.assertSequenceEqual(actual, expected)

    def test_where(self):
        def only_even(it):
            return it & 1 == 0

        actual = Slinkie(self.ITEMS).where(only_even).tuple()
        expected = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)

        self.assertTupleEqual(actual, expected)


class TestUtils(unittest.TestCase):
    LETTERS = 'abcdefgh'

    def test_first(self):
        actual = first(self.LETTERS)
        expected = self.LETTERS[0]
        self.assertEqual(actual, expected)

    def test_second(self):
        actual = second(self.LETTERS)
        expected = self.LETTERS[1]
        self.assertEqual(actual, expected)

    def test_third(self):
        actual = third(self.LETTERS)
        expected = self.LETTERS[2]
        self.assertEqual(actual, expected)

    def test_by_key(self):
        items = [{'letter': letter, 'number': number} for letter, number in zip(self.LETTERS, range(10))]
        get_letter = by_key('letter')
        actual = list(map(get_letter, items))
        expected = list(self.LETTERS)
        self.assertEqual(actual, expected)

    def test_by_keys(self):
        items = [{'letter': letter, 'number': number} for letter, number in zip(self.LETTERS, range(10))]
        get_letter = by_keys('number', 'letter')
        actual = list(map(get_letter, items))
        expected = list(zip(range(10), self.LETTERS))
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
