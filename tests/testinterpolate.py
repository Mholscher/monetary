#    Copyright 2023 Menno Hölscher
#
#    This file is part of monetary.

#    monetary is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    monetary is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.

#    You should have received a copy of the GNU Lesser General Public License
#    along with monetary.  If not, see <http://www.gnu.org/licenses/>.


import sys
import unittest
from datetime import date
from models.interpolate import interpolate

class TestInterpolation_calcs(unittest.TestCase):

    def test_doc_example(self):
        """ Over January report amount for two dates """


        start_data = (date(2023, 1, 1), 18000)
        end_data = (date(2023, 2, 1), 15000)
        dates = [date(2023, 1, 12), date(2023, 1, 24)]
        self.assertEqual(interpolate(start_data, end_data, dates),
                         [(date(2023,1,12),16935), (date(2023,1,24),15774)],
                         "Calculation error")

    def test_no_dates_request(self):
        """ No dates requested, no output """

        start_data = (date(2023, 1, 12), 1000)
        end_data = (date(2023, 1, 17), 5000)
        dates = []
        self.assertEqual(interpolate(start_data, end_data, dates),
                         [],
                         "Data returned for empty request")

    def test_date_outside_period_fails(self):
        """ Requesting a date outside the period fails. """

        start_data = (date(2023, 3, 11), 2000)
        end_data = (date(2023, 3, 28), 4500)
        dates = [date(2023, 4, 2)]
        with self.assertRaises(ValueError):
            values = interpolate(start_data, end_data, dates)
        dates = [date(2023, 3, 28)]
        with self.assertRaises(ValueError):
            values = interpolate(start_data, end_data, dates)
        dates = [date(2023, 1, 8)]
        with self.assertRaises(ValueError):
            values = interpolate(start_data, end_data, dates)

    def test_dates_ascending_order(self):
        """ Start and end date must be in ascending order """

        start_data = (date(2023, 1, 6), 6700)
        end_data = (date(2021, 1, 3), 9980)
        dates = [date(2022, 7, 5)]
        with self.assertRaises(ValueError):
            values = interpolate(start_data, end_data, dates)


if __name__ == '__main__' :
    unittest.main()
