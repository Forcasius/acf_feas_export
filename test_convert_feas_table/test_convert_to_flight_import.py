"""
Author: Markus W. Hofmann
Initial Date: May, 15. 2016

License: MIT

Description:

"""

import unittest
from convert_feas_tables.convert_to_flight_import import matches_filter, convert_time, convert_starttype


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

    def test_convert_time(self):
        self.assertEqual('01.04.2007 13:35', convert_time('04/01/2007', '12/30/1899 13:35:00'))
        self.assertEqual('14.05.2016 15:58', convert_time('05/14/2016', '12/30/1899 15:58:34'))

    def test_convert_starttype(self):
        self.assertEqual('1', convert_starttype('E'))
        self.assertEqual('3', convert_starttype('F'))
        self.assertEqual(None, convert_starttype('FAIL'))

if __name__ == '__main__':
    unittest.main()
