# -*- coding: utf-8 -*-

from src.SLIM.slimalgo import slim
import unittest


class SlimTest(unittest.TestCase):

    def test_iter0_nofail(self):
        ct = slim("easy_database", 0)
        self.assertTrue(True)

    def test_iter0_sct(self):
        ct = slim("easy_database", 0)
        print(ct)
        patterns = ct.order_by_standard_cover_order()
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
        self.assertEqual(patterns[0].usage_list, {[1, 2], [1, 2], [1, 2], [2]})
        self.assertEqual(patterns[1].usage_list, {[1, 2], [1, 2], [1, 2]})
        self.assertEqual(patterns[2].usage_list, {[4], [4]})
        self.assertEqual(patterns[3].usage_list, {[3]})
