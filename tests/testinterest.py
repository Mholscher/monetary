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
from models.interests import Interest, RunningInterest
#from helpers import calc_3_tenths

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
        """ We can create an interest amount """

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
        """ a negative interest is calculated """

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

    def test_start_month_december_is_january(self):
        """ Determine start of month after December is January 1st """

        from_date = date(year=2022, month=12, day=24)
        to_date = date(year=2023, month=1, day=12)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=17500, interest_frac=-0.045)
        self.assertEqual(interest_amount._som(from_date), date(2023, 1, 1),
                         "Start of month after December not January 1st")


class TestActualAndEqualPeriodInterest(unittest.TestCase):

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
        interest_amount.calculation_method = Interest.EQUAL_MONTHS
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
        interest_amount.calculation_method = Interest.EQUAL_MONTHS
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
        interest_amount.calculation_method = Interest.EQUAL_MONTHS
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
        interest_amount.calculation_method = Interest.EQUAL_MONTHS
        self.assertEqual(interest_amount.amount_cents(), 300000, 
                         "Interest not calculated correctly")

    def test_negative_interest(self):
        """ A negative interest is calculated """

        from_date = date(year=2022, month=3, day=1)
        to_date = date(year=2023, month=1, day=12)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=275000, interest_frac=-0.07,
                                   calculation_method=Interest.ACTUAL_PERIODS)
        self.assertEqual(interest_amount.amount_cents(), -17160, 
                         "Negative interest not calculated correctly")
        interest_amount.calculation_method = Interest.EQUAL_MONTHS
        self.assertEqual(interest_amount.amount_cents(), -17160, 
                         "Negative interest not calculated correctly")

    def test_interest_calendar_months(self):
        """ We can calculate interest based on calendar months """

        from_date = date(year=2022, month=3, day=21)
        to_date = date(year=2022, month=5, day=8)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=215000, interest_frac=0.06,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   calendar_months=True)
        self.assertEqual(interest_amount.amount_cents(), 1683, 
                         "Interest per calendar not correct")        
        interest_amount.calculation_method = Interest.EQUAL_MONTHS
        self.assertEqual(interest_amount.amount_cents(), 1612, 
                         "Interest per calendar equal months not correct")

    def test_compare_equal_months_equal_periods(self):
        """ Test difference at end of month """

        from_date = date(year=2022, month=2, day=28)
        to_date = date(year=2022, month=3, day=31)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=115000, interest_frac=1.0,
                                   calculation_method=Interest.ACTUAL_PERIODS)
        interest_amount_equal = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=115000, interest_frac=1.0,
                                   calculation_method=Interest.EQUAL_MONTHS)
        #print(interest_amount.amount_cents(), interest_amount_equal.amount_cents())
        self.assertTrue(interest_amount.amount_cents()
                        > interest_amount_equal.amount_cents(), 
                         "Not expected difference between methods")

    def test_short_period_calendar_month(self):
        """ Calculate interest for period within 1 month """

        from_date = date(year=2022, month=2, day=8)
        to_date = date(year=2022, month=2, day=21)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=120000, interest_frac=.12,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   calendar_months=True)
        self.assertEqual(interest_amount.amount_cents(), 513,
                         "Short period interest wrong")



class TestCompoundInterest(unittest.TestCase):

    def test_calculate_compound_interest(self):
        """ Calculate compound interest """

        from_date = date(year=2021, month=3, day=1)
        to_date = date(year=2021, month=5, day=1)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=50000, interest_frac=0.05,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 409, 
                         "Interest not compounded correctly")
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=50000, interest_frac=0.05,
                                   calculation_method=Interest.EQUAL_MONTHS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 409, 
                         "Interest not compounded correctly")

    def test_eom_dates(self):
        """ Compounding should handle day nos > 28 """

        from_date = date(year=2021, month=1, day=31)
        to_date = date(year=2021, month=3, day=31)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=160000, interest_frac=0.08,
                                   calculation_method=Interest.ACTUAL_DAYS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 2076, 
                         "Interest not compounded correctly")
        from_date = date(year=2021, month=3, day=31)
        to_date = date(year=2021, month=5, day=31)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=160000, interest_frac=0.08,
                                   calculation_method=Interest.ACTUAL_DAYS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 2146, 
                         "Interest not compounded correctly")
        from_date = date(year=2021, month=1, day=30)
        to_date = date(year=2021, month=3, day=30)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=160000, interest_frac=0.08,
                                   calculation_method=Interest.ACTUAL_DAYS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 2076, 
                         "Interest not compounded correctly")
        from_date = date(year=2021, month=1, day=29)
        to_date = date(year=2021, month=3, day=29)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=160000, interest_frac=0.08,
                                   calculation_method=Interest.ACTUAL_DAYS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 2076, 
                         "Interest not compounded correctly")

    def test_compound_over_1_year(self):
        """ Compounding by month should work for longer periods """

        from_date = date(year=2021, month=12, day=5)
        to_date = date(year=2023, month=2, day=10)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=1050000, interest_frac=0.09,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 112487, 
                         "Interest not compounded correctly")
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=1050000, interest_frac=0.09,
                                   calculation_method=Interest.EQUAL_MONTHS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 112487, 
                         "Interest not compounded correctly")
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=1050000, interest_frac=0.09,
                                   calculation_method=Interest.ACTUAL_DAYS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 117558, 
                         "Interest not compounded correctly")

    def test_compound_over_few_days(self):
        """ Compounding over less than a month works """

        from_date = date(year=2021, month=12, day=5)
        to_date = date(year=2021, month=12, day=10)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=12000, interest_frac=0.09,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly")
        self.assertEqual(interest_amount.amount_cents(), 15, 
                         "Interest compounded over short period not correct")
        interest_amount.calculation_method = Interest.EQUAL_MONTHS
        self.assertEqual(interest_amount.amount_cents(), 15, 
                         "Interest compounded over short period not correct")
        interest_amount.calculation_method = Interest.ACTUAL_DAYS
        self.assertEqual(interest_amount.amount_cents(), 15, 
                         "Interest compounded over short period not correct")

    def test_compounding_prorata_period(self):
        """ Calculate interest until a early next interest date """

        from_date = date(year=2021, month=12, day=5)
        to_date = date(year=2022, month=1, day=10)
        interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=35000, interest_frac=0.09,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly",
                                   next_interest_date=date(2021, 12, 24))
        self.assertEqual(interest_amount.amount_cents(), 311, 
                         "Interest compounded over short period not correct")

    def test_length_prorata_period(self):
        """ Early next interest date must be < 1 month away """

        from_date = date(year=2021, month=12, day=5)
        to_date = date(year=2022, month=1, day=10)
        with self.assertRaises(ValueError):
            interest_amount = Interest(from_date=from_date, to_date=to_date,
                                   start_balance=35000, interest_frac=0.09,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly",
                                   next_interest_date=date(2022, 1, 8))
            amount_cents = interest_amount.amount_cents()

    def test_next_compounding(self):
        """ Shift the next compounding date after compounding """

        from_date = date(year=2021, month=3, day=1)
        to_date = date(year=2021, month=5, day=1)
        interest = Interest(from_date=from_date, to_date=to_date,
                            start_balance=50000, interest_frac=0.05,
                            calculation_method=Interest.ACTUAL_PERIODS,
                            compound="monthly")
        interest_amount = interest.amount_cents()
        self.assertEqual(interest.next_interest_date, date(2021, 6, 1), 
                         "Next interest date not correct")



class TestChangingAmount(unittest.TestCase):

    def test_amount_change_mid_period(self):
        """ A principal changes mid-month """

        period_list = [{"from_date" : date(2021, 12, 1), 
                        "to_date" : date(2021, 12, 18),
                        "start_balance" : 120500,
                        "interest_frac" : 0.07},
                        {"from_date" : date(2021, 12, 18), 
                        "to_date" : date(2022, 1, 1),
                        "start_balance" : 123500,
                        "interest_frac" : 0.07}]
        interest = RunningInterest(period_list)
        self.assertEqual(interest.amount_cents(), 725,
                         "Incorrect amount calculated")

    def test_longer_than_1_month(self):
        """ When a period longer than one month is used """

        period_list = [{"from_date" : date(2021, 12, 2), 
                        "to_date" : date(2022, 1, 18),
                        "start_balance" : 120000,
                        "interest_frac" : 0.06},
                        {"from_date" : date(2022, 1, 19), 
                        "to_date" : date(2022, 2, 22),
                        "start_balance" : 123500,
                        "interest_frac" : 0.07}]
        interest = RunningInterest(period_list,
                                   calculation_method=Interest.ACTUAL_PERIODS)
        self.assertEqual(interest.amount_cents(), 1669,
                         "Incorrect amount calculated")

    def test_determine_next_interest_date(self):
        """ Find next interest date for running interest """

        period_list = [{"from_date" : date(2022, 7, 21), 
                        "to_date" : date(2022, 8, 18),
                        "start_balance" : 2230000,
                        "interest_frac" : 0.05},
                        {"from_date" : date(2022, 8, 19), 
                        "to_date" : date(2022, 10, 22),
                        "start_balance" : 2233000,
                        "interest_frac" : 0.05}]
        interest = RunningInterest(period_list,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly")
        amount_interest = interest.amount_cents()
        self.assertEqual(interest.next_interest_date, date(2022, 11, 21),
                         "Next compounding not set correctly")

    def test_running_with_compound_interest(self):
        """ Compound interest combined with running interest """

        period_list = [{"from_date" : date(2022, 8, 2), 
                        "to_date" : date(2022, 11, 18),
                        "start_balance" : 1130000,
                        "interest_frac" : 0.06},
                        {"from_date" : date(2022, 11, 19), 
                        "to_date" : date(2022, 12, 22),
                        "start_balance" : 1123500,
                        "interest_frac" : 0.07}]
        interest = RunningInterest(period_list,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly")
        self.assertEqual(interest.amount_cents(), 26718,
                         "Incorrect amount calculated")

    def test_one_period_no_compound(self):
        """ One period has no compounding interest date """

        period_list = [{"from_date" : date(2022, 8, 2), 
                        "to_date" : date(2022, 11, 18),
                        "start_balance" : 1130000,
                        "interest_frac" : 0.06},
                        {"from_date" : date(2022, 11, 19), 
                        "to_date" : date(2022, 11, 28),
                        "start_balance" : 1123500,
                        "interest_frac" : 0.07},
                        {"from_date" : date(2022, 11, 29), 
                        "to_date" : date(2022, 12, 22),
                        "start_balance" : 1123500,
                        "interest_frac" : 0.07}]
        interest = RunningInterest(period_list,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly")
        amount_interest = interest.amount_cents()
        self.assertEqual(interest.next_interest_date, date(2023, 1, 2),
                         "Wrong next interest date")
        interest = RunningInterest(period_list,
                                   calculation_method=Interest.ACTUAL_PERIODS,
                                   compound="monthly")
        self.assertEqual(interest.amount_cents(), 26494,
                         "Incorrect amount calculated")

 

if __name__ == '__main__' :
    unittest.main()
