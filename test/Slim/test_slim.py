# -*- coding: utf-8 -*-

from src.SLIM.slimalgo import slim
from src.Transaction import Transaction
import unittest


class SlimTest(unittest.TestCase):

    # chemin absolu
    def checkEqual(self, l1, l2):
        result = (len(l1) == len(l2))
        l1_list = sorted(l1, key=str)
        l2_list = sorted(l2, key=str)
        if result:
            for x in range(0, len(l1)-1):
                if not l1_list[x].otherequal(l2_list[x]):
                    result = False
        return result

    def test_iter0_nofail(self):
        ct = slim("easy_database", 0)
        self.assertTrue(True)

    def test_iter0_sct(self):
        ct = slim("easy_database", 0)
        patterns = ct.order_by_standard_cover_order()
        t1 = Transaction([1, 2])
        t2 = Transaction([2])
        t3 = Transaction([3])
        t4 = Transaction([4])
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        l1.append(t1.copy())
        l1.append(t1.copy())
        l1.append(t1.copy())
        l1.append(t2.copy())
        l2.append(t1.copy())
        l2.append(t1.copy())
        l2.append(t1.copy())
        l3.append(t4.copy())
        l3.append(t4.copy())
        l4.append(t3.copy())
        self.assertEqual(len(patterns), 4)
        self.assertEqual(patterns[0].elements, {2})
        self.assertEqual(patterns[1].elements, {1})
        self.assertEqual(patterns[2].elements, {4})
        self.assertEqual(patterns[3].elements, {3})
        self.assertEqual(patterns[0].usage, 4)
        self.assertEqual(patterns[1].usage, 3)
        self.assertEqual(patterns[2].usage, 2)
        self.assertEqual(patterns[3].usage, 1)
        self.assertEqual(patterns[0].support, 4)
        self.assertEqual(patterns[1].support, 3)
        self.assertEqual(patterns[2].support, 2)
        self.assertEqual(patterns[3].support, 1)
        self.assertTrue(self.checkEqual(patterns[0].usage_list, l1))
        self.assertTrue(self.checkEqual(patterns[1].usage_list, l2))
        self.assertTrue(self.checkEqual(patterns[2].usage_list, l3))
        self.assertTrue(self.checkEqual(patterns[3].usage_list, l4))

    def test_iter1_nofail(self):
        ct = slim("easy_database", 1)
        self.assertTrue(True)

    def test_iter1_len2(self):
        ct = slim("easy_database", 1)
        patterns = ct.order_by_standard_cover_order()
        t1 = Transaction([1, 2])
        t2 = Transaction([2])
        t3 = Transaction([3])
        t4 = Transaction([4])
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        l5 = []
        l1.append(t1.copy())
        l1.append(t1.copy())
        l1.append(t1.copy())
        l2.append(t2.copy())
        l4.append(t4.copy())
        l4.append(t4.copy())
        l5.append(t3.copy())
        self.assertEqual(len(patterns), 5)
        self.assertEqual(patterns[0].elements, {1, 2})
        self.assertEqual(patterns[1].elements, {2})
        self.assertEqual(patterns[2].elements, {1})
        self.assertEqual(patterns[3].elements, {4})
        self.assertEqual(patterns[4].elements, {3})
        self.assertEqual(patterns[0].usage, 3)
        self.assertEqual(patterns[1].usage, 1)
        self.assertEqual(patterns[2].usage, 0)
        self.assertEqual(patterns[3].usage, 2)
        self.assertEqual(patterns[4].usage, 1)
        self.assertEqual(patterns[0].support, 3)
        self.assertEqual(patterns[1].support, 4)
        self.assertEqual(patterns[2].support, 3)
        self.assertEqual(patterns[3].support, 2)
        self.assertEqual(patterns[4].support, 1)
        self.assertTrue(self.checkEqual(patterns[0].usage_list, l1))
        self.assertTrue(self.checkEqual(patterns[1].usage_list, l2))
        self.assertTrue(self.checkEqual(patterns[2].usage_list, l3))
        self.assertTrue(self.checkEqual(patterns[3].usage_list, l4))
        self.assertTrue(self.checkEqual(patterns[4].usage_list, l5))

    def test_itern_nofail(self):
        ct = slim("iris", 1000)
        self.assertTrue(True)

    def test_itern_res(self):
        ct = slim("iris", 1000)
        patterns = ct.order_by_standard_cover_order()
        self.assertTrue(len(patterns) <= 35)
        self.assertTrue(len(patterns) >= 25)
        self.assertEqual(patterns[0].elements, {6, 7, 8, 9, 10})
        self.assertEqual(patterns[0].usage, 37)
        self.assertEqual(patterns[0].support, 37)

    def test_iter1_tricky(self):
        ct = slim("tricky_database", 1)
        patterns = ct.order_by_standard_cover_order()
        self.assertTrue(len(patterns) == 5)
        t1 = Transaction([1])
        t2 = Transaction([2])
        t3 = Transaction([3, 4])
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        l1.append(t1.copy())
        l1.append(t1.copy())
        l1.append(t1.copy())
        l1.append(t1.copy())
        l2.append(t2.copy())
        l2.append(t2.copy())
        l2.append(t2.copy())
        l2.append(t2.copy())
        l3.append(t3.copy())
        l3.append(t3.copy())
        l3.append(t3.copy())
        self.assertEqual(len(patterns), 5)
        self.assertEqual(patterns[0].elements, {3, 4})
        self.assertEqual(patterns[1].elements, {1})
        self.assertEqual(patterns[2].elements, {2})
        self.assertEqual(patterns[3].elements, {3})
        self.assertEqual(patterns[4].elements, {4})
        self.assertEqual(patterns[0].usage, 3)
        self.assertEqual(patterns[1].usage, 4)
        self.assertEqual(patterns[2].usage, 4)
        self.assertEqual(patterns[3].usage, 0)
        self.assertEqual(patterns[4].usage, 0)
        self.assertEqual(patterns[0].support, 3)
        self.assertEqual(patterns[1].support, 4)
        self.assertEqual(patterns[2].support, 4)
        self.assertEqual(patterns[3].support, 3)
        self.assertEqual(patterns[4].support, 3)
        self.assertTrue(self.checkEqual(patterns[0].usage_list, l3))
        self.assertTrue(self.checkEqual(patterns[1].usage_list, l1))
        self.assertTrue(self.checkEqual(patterns[2].usage_list, l2))
        self.assertTrue(self.checkEqual(patterns[3].usage_list, l4))
        self.assertTrue(self.checkEqual(patterns[4].usage_list, l4))
