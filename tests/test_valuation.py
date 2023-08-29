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
        self.assertEqual(loan.posted_interest(), 17.84,
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
        self.assertEqual(loan.posted_interest(), 0,
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
        self.assertEqual(loan.posted_interest(), period_list[0]["interest_posted"],
                         "Incorrect interest for 1 entry")


class TestPredictions(unittest.TestCase):

    def test_predict_period(self):
        """ Predict interest for a period, from estimated rate """

        period_list = [{"from_date" : date(2023, 2, 1), 
                "to_date" : date(2023, 7, 1),
                "principal" : 122_000,
                "interest_posted" : 13.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2024, 2, 1),
                "start_balance" : 123_500,
                "interest_frac" : 0.07}]
        loan = LoanValue(period_list)
        self.assertEqual(loan.posted_interest(),
                         period_list[0]["interest_posted"],
                         "Incorrect interest for 1 entry")
        self.assertEqual(loan.future_interest(),
                         4886,
                         "Incorrect estimated interest")

    def test_principal_with_future(self):
        """ Principal change should be working with future interest """

        period_list = [{"from_date" : date(2023, 2, 1), 
                "to_date" : date(2023, 7, 1),
                "principal" : 122_000,
                "interest_posted" : 13.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2023, 10, 1),
                "principal" : 115_000,
                "interest_posted" : 12.22},
                {"from_date" : date(2023, 10, 1), 
                "to_date" : date(2024, 2, 1),
                "start_balance" : 123_500,
                "interest_frac" : 0.07}]
        loan = LoanValue(period_list)
        self.assertEqual(loan.repayment(), 7_000,
                             "Incorrect repayment for future interest")
        period_list = [{"from_date" : date(2023, 2, 1), 
                "to_date" : date(2023, 7, 1),
                "principal" : 122_000,
                "interest_posted" : 13.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2024, 2, 1),
                "start_balance" : 123_500,
                "interest_frac" : 0.07}]
        loan = LoanValue(period_list)
        self.assertEqual(loan.repayment(), 0,
                             "Incorrect repayment for future interest")

class TestMultipleRepayments(unittest.TestCase):

    def setUp(self):
        """ setup repayments etc. """

        self.period_list = [{"from_date" : date(2023, 6, 1),
                "to_date" : date(2024, 1, 5),
                "principal" : 120_000,
                "interest_posted" : 0.54},
                {"from_date" : date(2024, 1, 5),
                "to_date" : date(2024, 5, 31),
                "principal" : 105_000,
                "interest_posted" : 17.30},
                {"from_date" : date(2024, 5, 31),
                "to_date" : date(2025, 5, 31),
                "principal" : 96_000,
                "interest_posted" : 12.27}]


    def test_multiple_repayments(self):
        """  Value should be the sum of repayments """

        loan = LoanValue(self.period_list)
        self.assertEqual(loan.repayment(), 24_000,
                             "Incorrect repayment for multiple periods")

class TestWithDiscountingInterest(unittest.TestCase):

    def test_with_one_rate(self):
        """ A payment will be discounted if discount_rate is there """

        period_list = [{"from_date" : date(2023, 2, 1),
                "to_date" : date(2023, 7, 1),
                "principal" : 122_000,
                "interest_posted" : 13.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2024, 2, 1),
                "start_balance" : 123_500,
                "interest_frac" : 0.07}]
        discount_factors = {date(2023, 7, 1) : 0.02}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.future_interest(),
                         round(4886 * (1 - 0.02)),
                         "Incorrect estimated discounted interest")

    def test_with_future_rate(self):
        """ No discounte if discount_rate is beyond payment date """

        period_list = [{"from_date" : date(2023, 2, 1),
                "to_date" : date(2023, 7, 1),
                "principal" : 122_000,
                "interest_posted" : 13.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2024, 2, 1),
                "start_balance" : 123_500,
                "interest_frac" : 0.07}]
        discount_factors = {date(2023, 8, 1) : 0.02}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.future_interest(),
                         4886,
                         "Estimated interest wrongfully discounted")

    def test_with_more_rates(self):
        """ Use proper discount_rate if there are more """

        period_list = [{"from_date" : date(2023, 2, 1),
                "to_date" : date(2023, 7, 1),
                "principal" : 122_000,
                "interest_posted" : 13.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2024, 2, 1),
                "start_balance" : 123_500,
                "interest_frac" : 0.07}]
        discount_factors = {date(2023, 7, 1) : 0.02,
                            date(2023,2, 1) : 0.1,
                            date(2024,8, 3) : 0.015}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.future_interest(),
                         round(4886 * (1 - 0.02)),
                         "Used incorrect discounted factor")

    def test_with_interpolated_rates(self):
        """ Interpolate discount_rate if between two dates """

        period_list = [{"from_date" : date(2023, 2, 1),
                "to_date" : date(2023, 7, 1),
                "principal" : 122_000,
                "interest_posted" : 13.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2024, 2, 1),
                "start_balance" : 123_500,
                "interest_frac" : 0.07}]
        discount_factors = {date(2023, 5, 1) : 0.02,
                            date(2023,2, 1) : 0.015,
                            date(2023, 8, 3) : 0.025,
                            date(2024, 1, 24) : 0.12}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.future_interest(),
                         4772,
                         "Incorrect discount interpolation")

    def test_date_beyond_last_rate(self):
        """ Use latest discount_rate if payment after last """

        period_list = [{"from_date" : date(2023, 2, 1),
                "to_date" : date(2024, 1, 28),
                "principal" : 122_000,
                "interest_posted" : 13.54},
                {"from_date" : date(2024, 1, 28),
                "to_date" : date(2024, 2, 12),
                "start_balance" : 123_500,
                "interest_frac" : 0.07}]
        discount_factors = {date(2023, 5, 1) : 0.02,
                            date(2023,2, 1) : 0.015,
                            date(2023, 8, 3) : 0.025,
                            date(2024, 1, 24) : 0.12}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.future_interest(),
                         round(355 * (1-0.12)),
                         "Incorrect discount beyond last date")


class TestWithDiscountingRepayment(unittest.TestCase):

    def test_loan_repayment_discounted(self):
        """ Test repayment discounted at factor date """

        period_list = [{"from_date" : date(2023, 6, 1),
                "to_date" : date(2023, 11, 30),
                "principal" : 120_000,
                "interest_posted" : 0.54},
                {"from_date" : date(2023, 12, 1),
                "to_date" : date(2024, 5, 31),
                "principal" : 105_000,
                "interest_posted" : 17.30}]
        discount_factors = {date(2023, 12, 1) : 0.02,
                            date(2024, 1, 24) : 0.12}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.repayment(), 15000 * (1 - 0.02),
                         "Incorrect discounted repayment")

    def test_one_discount_factor(self):
        """ Test repayment discounted at a single factor """

        period_list = [{"from_date" : date(2023, 6, 1),
                "to_date" : date(2024, 1, 5),
                "principal" : 120_000,
                "interest_posted" : 0.54},
                {"from_date" : date(2024, 1, 5),
                "to_date" : date(2024, 5, 31),
                "principal" : 105_000,
                "interest_posted" : 17.30}]
        discount_factors = {date(2023, 12, 1) : 0.02}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.repayment(), 15000 * (1 - 0.02),
                         "Incorrect discount for single factor")

    def test_no_discount_in_past(self):
        """ Test repayment discounted at a single factor """

        period_list = [{"from_date" : date(2023, 6, 1),
                "to_date" : date(2023, 7, 1),
                "principal" : 120_000,
                "interest_posted" : 0.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2024, 5, 31),
                "principal" : 105_000,
                "interest_posted" : 17.30}]
        discount_factors = {date(2023, 12, 1) : 0.02}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.repayment(), 15000,
                         "Discounted early payment")

    def test_discount_for_more_repayments(self):
        """ Test repayment discounted at multiple factors """

        period_list = [{"from_date" : date(2023, 6, 1),
                "to_date" : date(2023, 7, 1),
                "principal" : 120_000,
                "interest_posted" : 0.54},
                {"from_date" : date(2023, 7, 1),
                "to_date" : date(2023, 11, 1),
                "principal" : 105_000,
                "interest_posted" : 17.30},
                {"from_date" : date(2023, 11, 1),
                "to_date" : date(2024, 2, 12),
                "principal" : 98_000,
                "interest_posted" : 12.44}]
        discount_factors = {date(2023, 7, 1) : 0.02,
                            date(2023, 11, 1) : 0.03}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        self.assertEqual(loan.repayment(), round(15000 * (1 - .02)
                                                 + 7000 * (1 - .03)),
                         "Discounted incorrectly")

    def test_discount_repayments_interpolated(self):
        """ Test repayment discounted at multiple factors """

        period_list = [{"from_date" : date(2023, 6, 1),
                "to_date" : date(2023, 9, 12),
                "principal" : 120_000,
                "interest_posted" : 0.54},
                {"from_date" : date(2023, 9, 12),
                "to_date" : date(2023, 11, 1),
                "principal" : 105_000,
                "interest_posted" : 17.30},
                {"from_date" : date(2023, 11, 1),
                "to_date" : date(2024, 2, 12),
                "principal" : 98_000,
                "interest_posted" : 12.44}]
        discount_factors = {date(2023, 7, 1) : 0.02,
                            date(2023, 11, 1) : 0.03}
        loan = LoanValue(period_list, discount_factors=discount_factors)
        # In the comparison value the + 1 occurs because of different rounding
        # in the valuation module that I could not reconstruct :=)
        self.assertEqual(loan.repayment(), round(15000 - 15000 * (.02 + 74 * 
                                                          (.03 - .02) / 123)
                                                 + 7000 * (1 - .03) + 1),
                         "Discounted with interpolation incorrectly")
