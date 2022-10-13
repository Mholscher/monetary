#    Copyright 2022 Menno Hölscher
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
from datetime import date, timedelta
from models.interests import Interest

class TestActualDaysInterest(unittest.TestCase):

    def setUp(self):

        self.int_calc = Interest

    def test_month_case(self):
        """ Calculate a month of interest """

        interest_amount = self.int_calc.calc_month(1500, .05)
        self.assertEqual(interest_amount, 6,
                         "Interest amount wrong")

    def test_year_interest(self):
        """ Calculate a year of interest """

        interest_amount = self.int_calc.calc_year(1500, .1)
        self.assertEqual(interest_amount, 150,
                         "Interest amount wrong")

    def test_create_interest(self):
        """ We can create in interest amount """

        from_date = date(year=2021, month=12, day=1)
        to_date = date(year=2022, month=1, day=15)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=15000, interest_frac=0.1)
        self.assertTrue(interest_amount, "No amount calculated")
        self.assertEqual(interest_amount.amount_cents(), 185,
                         "Incorrect amount")

    def test_change_interest(self):
        """ Changing interest data changes interest amount """

        from_date = date(year=2021, month=11, day=1)
        to_date = date(year=2022, month=7, day=15)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=105000, interest_frac=0.2)
        self.assertTrue(interest_amount, "No amount calculated")
        self.assertEqual(interest_amount.amount_cents(), 14729,
                         "Incorrect first amount")
        interest_amount.interest_frac = 0.3
        self.assertEqual(interest_amount.amount_cents(), 22093,
                         "Incorrect amount after interest change")
        interest_amount.start_balance = 210000
        self.assertEqual(interest_amount.amount_cents(), 44186,
                         "Incorrect amount after balance change")
        interest_amount.to_date = date(year=2022, month=11, day=5)
        self.assertEqual(interest_amount.amount_cents(), 63690,
                         "Incorrect amount after date change")

    def test_zero_interest(self):
        """ Zero rate should return zero interest """

        from_date = date(year=2022, month=3, day=1)
        to_date = date(year=2022, month=11, day=30)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=150000, interest_frac=0.0)
        self.assertEqual(interest_amount.amount_cents(), 0, 
                         "Interest for zero percentage not zero")

    def test_extreme_interest(self):
        """ extremely high percentage is calculated """

        from_date = date(year=2022, month=3, day=1)
        to_date = date(year=2023, month=3, day=1)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=150000, interest_frac=2.0)
        self.assertEqual(interest_amount.amount_cents(), 300000, 
                         "Interest not calculated correctly")

    def test_negative_interest(self):
        """ extremely high percentage is calculated """

        from_date = date(year=2022, month=3, day=1)
        to_date = date(year=2023, month=1, day=12)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=175000, interest_frac=-0.05)
        self.assertEqual(interest_amount.amount_cents(), -7599, 
                         "Negative interest not calculated correctly")

    def test_dates_order(self):
        """ The to date must be on or after the from date """

        from_date = date(year=2032, month=3, day=1)
        to_date = date(year=2023, month=1, day=12)
        with self.assertRaises(ValueError):
            interest_amount = Interest(from_date=from_date,
                                       to_date=to_date,
                                       start_balance=155000,
                                       interest_frac=0.05)


class TestActualPeriodInterest(unittest.TestCase):

    def test_create_interest(self):
        """ We can create in interest amount using actual periods """

        from_date = date(year=2021, month=12, day=1)
        to_date = date(year=2022, month=1, day=15)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=15000, interest_frac=0.1,
                                   calculation_method=Interest.ACTUAL_PERIODS)
        self.assertTrue(interest_amount, "No amount calculated")
        self.assertEqual(interest_amount.amount_cents(), 178,
                         "Incorrect amount")

    def test_long_period(self):
        """ Create an interest for a period over a year """

        from_date = date(year=2021, month=12, day=1)
        to_date = date(year=2023, month=1, day=3)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=144000, interest_frac=0.08,
                                   calculation_method=Interest.ACTUAL_PERIODS)
        self.assertTrue(interest_amount, "No amount calculated")
        self.assertEqual(interest_amount.amount_cents(), 12510,
                         "Incorrect amount")

    def test_less_than_1_month(self):
        """ Create interest amount for a few days """

        from_date = date(year=2021, month=12, day=1)
        to_date = date(year=2021, month=12, day=15)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=75000, interest_frac=0.12,
                                   calculation_method=Interest.ACTUAL_PERIODS)
        self.assertTrue(interest_amount, "No amount calculated")
        self.assertEqual(interest_amount.amount_cents(), 345,
                         "Incorrect amount")

    def test_zero_interest(self):
        """ Zero rate should return zero interest """

        from_date = date(year=2022, month=4, day=6)
        to_date = date(year=2022, month=10, day=30)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=150000, interest_frac=0.0)
        self.assertEqual(interest_amount.amount_cents(), 0, 
                         "Interest for zero percentage not zero")

    def test_extreme_interest(self):
        """ extremely high percentage is calculated """

        from_date = date(year=2022, month=3, day=1)
        to_date = date(year=2023, month=3, day=1)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=150000, interest_frac=2.0)
        self.assertEqual(interest_amount.amount_cents(), 300000, 
                         "Interest not calculated correctly")

    def test_negative_interest(self):
        """ extremely high percentage is calculated """

        from_date = date(year=2022, month=3, day=1)
        to_date = date(year=2023, month=1, day=12)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=275000, interest_frac=-0.07,
                                   calculation_method=Interest.ACTUAL_PERIODS)
        self.assertEqual(interest_amount.amount_cents(), -17160, 
                         "Negative interest not calculated correctly")

if __name__ == '__main__' :
    unittest.main()
