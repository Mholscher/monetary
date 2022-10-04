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

class Test(unittest.TestCase):

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
        self.assertEqual(interest_amount.amount_cents(), 2,
                         "Incorrect amount")

    def test_change_interest(self):
        """ Changing interest data changes interest amount """

        from_date = date(year=2021, month=11, day=1)
        to_date = date(year=2022, month=7, day=15)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=105000, interest_frac=0.2)
        self.assertTrue(interest_amount, "No amount calculated")
        self.assertEqual(interest_amount.amount_cents(), 147,
                         "Incorrect first amount")
        interest_amount.interest_frac = 0.3
        self.assertEqual(interest_amount.amount_cents(), 221,
                         "Incorrect amount after interest change")
        interest_amount.start_balance = 210000
        self.assertEqual(interest_amount.amount_cents(), 442,
                         "Incorrect amount after balance change")
        interest_amount.to_date = date(year=2022, month=11, day=5)
        self.assertEqual(interest_amount.amount_cents(), 637,
                         "Incorrect amount after date change")


if __name__ == '__main__' :
    unittest.main()
