"""
Author: Markus W. Hofmann
Initial Date: May, 15. 2016

License: MIT

Description:

"""

import unittest
from convert_feas_tables.convert_to_flight_import import matches_filter, convert_time, convert_starttype, convert_type, \
    convert_charge


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

    def test_convert_type(self):
        self.assertEqual('15', convert_type('F'))  # Fremdflug
        self.assertEqual('4', convert_type('G'))  # Passagierflug == Gastflug
        self.assertEqual('14', convert_type('L'))  # Luftrettung
        self.assertEqual('10', convert_type('N'))  # Normalflug == Privatflug
        self.assertEqual('3', convert_type('R'))
        self.assertEqual('8', convert_type('S'))
        self.assertEqual('13', convert_type('V'))  # Vereinsflug
        self.assertEqual('2', convert_type('W'))
        self.assertEqual(None, convert_type('Q'))

    def test_convert_charge(self):
        self.assertEqual('1', convert_charge('F'))  # Fremdflug -> Rechnung
        self.assertEqual('4', convert_charge('G'))  # Passagierflug
        self.assertEqual('1', convert_charge('L'))  # Luftrettung -> Rechnung
        self.assertEqual('2', convert_charge('N'))  # Normalflug == Privatflug
        self.assertEqual('2', convert_charge('R'))
        self.assertEqual('2', convert_charge('S', {'Begleiter': ''}))
        self.assertEqual('3', convert_charge('S', {'Begleiter': 'Name'}))
        self.assertEqual('1', convert_charge('V'))  # Vereinsflug == keine Rechnung
        self.assertEqual('1', convert_charge('W'))  # Werstattflug -> Verein zahlt
        self.assertEqual(None, convert_charge('Q'))


if __name__ == '__main__':
    unittest.main()
