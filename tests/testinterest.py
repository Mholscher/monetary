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
from models.interests import interest

class Test(unittest.TestCase):

    def setUp(self):

        self.int_calc = interest()

    def test_month_case(self):
        """ Calculate a month of interest """

        interest_amount = self.int_calc.calc_month(1500, .1)
        self.assertEqual(interest_amount, 2,
                         "Interest amount wrong")

    def test_year_interest(self):
        """ Calculate a year of interest """

        interest_amount = self.int_calc.calc_year(1500, .1)
        self.assertEqual(interest_amount, 150,
                         "Interest amount wrong")


if __name__ == '__main__' :
    unittest.main()
