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
from datetime import date
import unittest
from monetary_models.valuation import LoanValue

class TestThisMonthValue(unittest.TestCase):

    def test_compile_interest(self):
        """ Compile the value from posted interest """

        period_list = [{"from_date" : date(2023, 6, 1), 
                "to_date" : date(2023, 11, 30),
                "principal" : 120_000,
                "interest_posted" : 0.54},
                {"from_date" : date(2023, 12, 1), 
                "to_date" : date(2024, 5, 31),
                "principal" : 105_000,
                "interest_posted" : 17.30}]
        loan = LoanValue(period_list)
        self.assertEqual(loan.interest(), 17.84,
                         "Incorrect interest")

    def test_principal_change(self):
        """ Compile the value from posted interest """

        period_list = [{"from_date" : date(2023, 6, 1), 
                "to_date" : date(2023, 11, 30),
                "principal" : 120_000,
                "interest_posted" : 0.54},
                {"from_date" : date(2023, 12, 1), 
                "to_date" : date(2024, 5, 31),
                "principal" : 105_000,
                "interest_posted" : 17.30}]
        loan = LoanValue(period_list)
        self.assertEqual(loan.repayment(), period_list[0]["principal"]
                         - period_list[1]["principal"],
                         "Incorrect repayment")
        period_list.append({"from_date" : date(2023, 6, 1), 
                "to_date" : date(2024, 7, 31),
                "principal" : 102_000,
                "interest_posted" : 8.30})
        loan = LoanValue(period_list)
        self.assertEqual(loan.repayment(), period_list[0]["principal"]
                         - period_list[2]["principal"],
                         "Incorrect repayment for 3 entries")

    def test_return_zero_amounts(self):
        """ No posted amounts (principal change & interest) return 0 """

        period_list = []
        loan = LoanValue(period_list)
        self.assertEqual(loan.interest(), 0,
                         "Interest not 0 for no data")
        self.assertEqual(loan.repayment(), 0,
                         "Repayment not 0 for no data")

    def test_one_period_only(self):
        """ One period should return interest and zero for repayment """

        period_list = [{"from_date" : date(2023, 6, 1), 
                "to_date" : date(2023, 11, 30),
                "principal" : 120_000,
                "interest_posted" : 0.54}]
        loan = LoanValue(period_list)
        self.assertEqual(loan.repayment(), 0,
                         "Incorrect repayment for 1 entry")
        loan = LoanValue(period_list)
        self.assertEqual(loan.interest(), period_list[0]["interest_posted"],
                         "Incorrect interest for 1 entry")


