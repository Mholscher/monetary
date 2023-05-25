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
from monetary_models import deprecate_example as ex

class TestDeprecate_recalc(unittest.TestCase):

    def test_deprecation_schedule(self):
        """ Setup a schedule for recalculating deprecation """

        deprecation_schedule =\
            ex.RecalcDeprecationSchedule(120000,
                                         purchase_date=date(2023, 1, 1),
                                         first_reporting_date=
                                         date(2023, 1, 1),
                                         deprecate_years=6)
        self.assertEqual(deprecation_schedule.amounts[2][1], 20000,
                         "Wrong amount first year at start")

    def test_second_deprecation(self):
        """ Test recalculation after changed replacement amount """

        deprecation_schedule =\
            ex.RecalcDeprecationSchedule(120000,
                                         date(2023, 1, 1),
                                         first_reporting_date=
                                         date(2023, 1, 1),
                                         calculation_date=
                                         date(2024, 1, 1),
                                         previous_yearly_deprecation=
                                         20000,
                                         replacement_value=
                                         140000,
                                         deprecate_years=6)
        self.assertEqual(deprecation_schedule.new_amounts[3][1], 23333,
                         "Wrong amount second year")

    def test_correct_previous_period(self):
        """ If a valuation is changed, previous period(s) are updated """

        deprecation_schedule =\
            ex.RecalcDeprecationSchedule(120000,
                                         date(2023, 1, 1),
                                         first_reporting_date=
                                         date(2023, 1, 1),
                                         calculation_date=
                                         date(2024, 1, 1),
                                         previous_yearly_deprecation=20000,
                                         replacement_value=
                                         140000,
                                         deprecate_years=6)
        self.assertEqual(deprecation_schedule.correction(),
                         3333,
                         "incorrect correction")

    def test_no_correction_needed(self):
        """ If no change yet, no correction needed """

        deprecation_schedule =\
            ex.RecalcDeprecationSchedule(120000,
                                         date(2023, 1, 1),
                                         first_reporting_date=
                                         date(2023, 1, 1),
                                         calculation_date=
                                         date(2024, 1, 1),
                                         deprecate_years=6)
        self.assertEqual(deprecation_schedule.correction(),
                         0,
                         "No correction should be present")
        

class TestBeyondSecondYear(unittest.TestCase):

    def test_third_year_deprecation(self):
        """ Next period deprecation """

        deprecation_schedule =\
            ex.RecalcDeprecationSchedule(120000,
                                         date(2023, 1, 1),
                                         first_reporting_date=
                                         date(2023, 1, 1),
                                         calculation_date=
                                         date(2025, 1, 1),
                                         previous_yearly_deprecation=23333,
                                         replacement_value=
                                         132000,
                                         deprecate_years=6)
        self.assertEqual(deprecation_schedule.new_amounts[3][1], 22000,
                         "Wrong amount later year")
        self.assertEqual(deprecation_schedule.correction(),
                         -2666,
                         "incorrect correction later year")
    def test_before_revalue(self):
        """ Deprecation for 9 years with all issues """

        deprecation_schedule =\
            ex.RecalcDeprecationSchedule(117000,
                                         date(2022, 6, 1),
                                         first_reporting_date=
                                         date(2023, 1, 1),
                                         calculation_date=
                                         date(2023, 1, 1),
                                         replacement_value=
                                         117000,
                                         value_at_end=3000,
                                         deprecate_years=9)
        self.assertEqual(deprecation_schedule.amounts[1][1], 7389,
                         "Wrong amount pro rata period")
        self.assertEqual(deprecation_schedule.new_amounts[1][1], 7389,
                         "Wrong amount pro rata period")
        self.assertEqual(deprecation_schedule.new_amounts[2][1], 12667,
                         "Wrong amount first period")
        self.assertEqual(deprecation_schedule.correction(), 0,
                         "Correction after no revalue")

    def test_after_revalue(self):
        """ Deprecation for 9 years with all issues """

        deprecation_schedule =\
            ex.RecalcDeprecationSchedule(117000,
                                         date(2022, 6, 1),
                                         first_reporting_date=
                                         date(2023, 1, 1),
                                         calculation_date=
                                         date(2025, 1, 1),
                                         previous_yearly_deprecation=12667,
                                         replacement_value=
                                         123000,
                                         value_at_end=3000,
                                         deprecate_years=9)
        self.assertEqual(deprecation_schedule.amounts[4][1], 12667,
                         "Wrong amount pro rata period")
        self.assertEqual(deprecation_schedule.new_amounts[4][1], 13333,
                         "Wrong amount period of recalculation")
        self.assertEqual(deprecation_schedule.correction(), 1721,
                         "Correction incorrect after revalue")

class TestCheckParameters(unittest.TestCase):

    def test_no_replacement_value_at_purchase(self):
        """ Cannot have replacement value at purchase """

        with self.assertRaises(ValueError):
            deprecation_schedule =\
                ex.RecalcDeprecationSchedule(155000,
                                            date(2022, 8, 3),
                                            first_reporting_date=
                                            date(2023, 1, 1),
                                            calculation_date=
                                            date(2022, 8, 3),
                                            replacement_value=
                                            163000,
                                            value_at_end=3800,
                                            deprecate_years=10)

    def test_no_previous_year_deprecation(self):
        """ At start there cannot be previous year deprecation  """

        with self.assertRaises(ValueError):
            deprecation_schedule =\
                ex.RecalcDeprecationSchedule(175000,
                                            date(2022, 7, 3),
                                            first_reporting_date=
                                            date(2023, 1, 1),
                                            calculation_date=
                                            date(2022, 7, 3),
                                            previous_yearly_deprecation=
                                            12000,
                                            value_at_end=3800,
                                            deprecate_years=10)

    def test_calculation_before_purchase(self):
        """ The calculation date is before the purchase date """

        deprecation_schedule =\
            ex.RecalcDeprecationSchedule(188000,
                                        date(2023, 2, 1),
                                        first_reporting_date=
                                        date(2024, 1, 1),
                                        calculation_date=
                                        date(2023, 2, 1),
                                        value_at_end=3800,
                                        deprecate_years=10)
        self.assertEqual(deprecation_schedule.value_at(date(2022, 10, 1)),
                         0,
                         "Value before purchase calculated")
                                                       
