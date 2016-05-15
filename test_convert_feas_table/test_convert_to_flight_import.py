"""
Author: Markus W. Hofmann
Initial Date: May, 15. 2016

License: MIT

Description:

"""

import unittest
from convert_feas_tables.convert_to_flight_import import matches_filter


class ConvertToFlightImportTestCase(unittest.TestCase):
    def test_matches_filter(self):
        my_filter = ('SDate', ['2014', '2015'])
        self.assertEqual(True, matches_filter({'Foo': 'bar', 'SDate': '2/03/2014', 'Baz': 'fbar'}, my_filter))
        self.assertEqual(True, matches_filter({'Foo': 'bar', 'SDate': '2/03/2015', 'Baz': 'fbar'}, my_filter))
        self.assertEqual(False, matches_filter({'Foo': 'bar', 'SDate': '2/03/1011', 'Baz': 'fbar'}, my_filter))
        self.assertEqual(False, matches_filter({'Foo': 'bar', 'SDate': '2/03/2013', 'Baz': 'fbar'}, my_filter))
        self.assertEqual(False, matches_filter({'Foo': 'bar', 'SDate': '2/03/2016', 'Baz': 'fbar'}, my_filter))

    def test_matches_filter_with_no_filter_criteria(self):
        my_filter = ('FAIL', ['2014', '2015'])
        self.assertEqual(False, matches_filter({'Foo': 'bar', 'SDate': '2/03/2014', 'Baz': 'fbar'}, my_filter))
        self.assertEqual(False, matches_filter({'Foo': 'bar', 'SDate': '2/03/2015', 'Baz': 'fbar'}, my_filter))
        self.assertEqual(False, matches_filter({'Foo': 'bar', 'SDate': '2/03/1011', 'Baz': 'fbar'}, my_filter))
        self.assertEqual(False, matches_filter({'Foo': 'bar', 'SDate': '2/03/2013', 'Baz': 'fbar'}, my_filter))
        self.assertEqual(False, matches_filter({'Foo': 'bar', 'SDate': '2/03/2016', 'Baz': 'fbar'}, my_filter))

    def test_matches_filter_with_no_filter(self):
        self.assertEqual(True, matches_filter({'Foo': 'bar', 'SDate': '2/03/2014', 'Baz': 'fbar'}, None))


if __name__ == '__main__':
    unittest.main()
