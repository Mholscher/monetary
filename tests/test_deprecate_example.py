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
                                         date(2023, 1, 1),
                                         first_reporting_date=
                                         date(2023, 1, 1),
                                         deprecate_years=6)
        print(deprecation_schedule.amounts)
        self.assertEqual(deprecation_schedule.amounts[1][1], 20000,
                         "Wrong amount first year at start")
        
