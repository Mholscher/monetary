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

""" This module contains tests for the deprecation model
    """

import sys
import unittest
from datetime import date
from dateutil.relativedelta import relativedelta
from models.deprecate import DeprecationSchedule

class TestDeprecation(unittest.TestCase):

    def setUp(self):

        self.schedule = DeprecationSchedule(15000000, date(2022, 12, 4),
                                       date(2023, 1,1), 5)

    def test_first_period(self):
        """ Calculate the first period of linear deprecation """

        self.assertEqual(self.schedule.amounts[0][1], 0, 
                         "First period incorrect")

    def test_next_periods(self):
        """ Calculate subsequent periods """

        self.assertEqual(self.schedule.amounts[1][1], 250000, 
                         "Second period amount incorrect")
        self.assertEqual(self.schedule.amounts[1][0], date(2023,1,1), 
                         "Second period date incorrect")
        self.assertEqual(self.schedule.amounts[2][1], 3000000, 
                         "Third period amount incorrect")
        self.assertEqual(self.schedule.amounts[2][0], date(2024,1,1), 
                         "Third period date incorrect")

    def test_first_reporting_date(self):
        """ First reporting date cannot be more than 12 months from now """

        with self.assertRaises(ValueError):
            self.schedule = DeprecationSchedule(10000, date(2022, 12, 4),
                                                date(2024, 1,1), 5)

    def test_purchase_on_reporting_date(self):
        """ The asset is purchased on reporting date """

        self.schedule = DeprecationSchedule(5200000, date(2022, 1, 1),
                                       date(2022, 1,1), 5)        
        self.assertEqual(self.schedule.amounts[0][1], 0, 
                         "Period start on reporting date incorrect")

    def test_value_at_date(self):
        """ A value reported at a date takes deprecation into account """

        self.assertEqual(self.schedule.value_at(self.schedule.purchase_date),
                         15000000,
                         "Wrong amount at start")
        date_at = self.schedule.purchase_date + relativedelta(years=1)
        self.assertEqual(self.schedule.value_at(date_at),
                         14750000,
                         "Wrong amount after 1 year")

    def test_after_deprecation_value_zero(self):
        """ No value after deprecationperiod """

        after_deprecation = (self.schedule.purchase_date +
                             relativedelta(years=6))
        self.assertEqual(self.schedule.value_at(after_deprecation), 0,
                         "Value not deprecated to zero")

    def test_date_long_after_end(self):
        """ Remaining value well... remains """

        far_future = (self.schedule.purchase_date +
                      relativedelta(years=12))
        self.assertEqual(self.schedule.value_at(far_future), 0,
                         "In far future wrong amount")

    def test_with_end_value(self):
        """ Can specify an end value """

        schedule = DeprecationSchedule(120000, date(2022, 12, 17),
                                       date(2023, 1,1), 6, 4500)
        self.assertEqual(schedule.value_at(date(2031, 2, 2)), 4500,
                         "Value after deprecation incorrect")
        self.assertEqual(schedule.value_at(date(2040, 2, 2)), 4500,
                         "Value long after deprecation incorrect")

    def test_with_other_reporting_date(self):
        """ The reporting dates are not on the first of January """

        schedule = DeprecationSchedule(220000, date(2023, 2, 20),
                                       date(2023, 4,1), 9)
        self.assertEqual(schedule.value_at(date(2025, 8, 2)), 167038,
                         "Value after deprecation incorrect")
        
